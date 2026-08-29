from enum import Enum, StrEnum
from importlib.metadata import version

import typer

from cmt.ai.openai import OpenAIProvider
from cmt.analysis.analyzer import Analyzer
from cmt.config.settings import Config, Settings
from cmt.exceptions import CmtError
from cmt.git.repository import Repository
from cmt.utils import edit_with_vim

app = typer.Typer(
    add_completion=False,
)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"cmt-cli version: {version('cmt-cli')}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    flag: bool = typer.Option(False, "--version", callback=version_callback, is_eager=True),
) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=0)


@app.command()
def suggest() -> None:
    """Suggest a commit message based on staged changes."""
    try:
        repository = Repository()
        analyzer = Analyzer()

        if not repository.is_git_repository():
            raise CmtError("Not a git repository.")

        staged_files = repository.get_staged_changes()

        if not staged_files.files:
            typer.echo(
                "No staged files found. Please stage your changes before running this command."
            )
            raise typer.Exit(code=0)

        analysis_result = analyzer.analyze(staged_files)

        open_ai = OpenAIProvider()

        commit = open_ai.generate_commit_message(staged_files, analysis_result)
        commit_command = OpenAIProvider.commit_command(commit)

        typer.echo(f"Suggested commit:\n\n{commit_command}")

        while True:
            action = (
                typer.prompt("\nUse this message? [y]es / [e]dit / [n]o", default="y")
                .strip()
                .lower()[0]
            )

            if action == "n":
                typer.echo("Aborted.")
                break

            if action == "e":
                commit_command = edit_with_vim(commit_command)
                typer.echo(f"Edited commit:\n\n{commit_command}")

            if action == "y":
                result = repository.commit(commit_command)
                typer.echo(f"Commit result:\n\n{result.stdout}")
                break

    except CmtError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1) from None
    except typer.Exit:
        raise
    except KeyboardInterrupt:
        typer.echo("\nOperation cancelled by user.", err=True)
        raise typer.Exit(code=1) from None
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=1) from None


class ConfigTask(StrEnum):
    set = "set"
    get = "get"


@app.command()
def config(task: ConfigTask) -> None:
    """Configure cmt-cli configuration for OpenAI API key and model."""
    if task == ConfigTask.set:
        settings = Settings()

        open_ai_key = typer.prompt("Enter your OpenAI API key", default=None)
        open_ai_model = typer.prompt(
            "Enter your OpenAI model", default=settings.OPEN_AI_DEFAULT_MODEL
        )
        settings.set(Config(api_key=open_ai_key, model=open_ai_model))

    if task == ConfigTask.get:
        settings = Settings()
        setting_values = settings.get()

        if setting_values.api_key:
            typer.echo(f"OpenAI API key: {setting_values.api_key[:10]} ****")

        if setting_values.model:
            typer.echo(f"OpenAI model: {setting_values.model}")

        raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
