import typer

from cmt.ai.openai import OpenAIProvider
from cmt.analysis.analyzer import Analyzer
from cmt.config.settings import OpenAIConfig, Settings
from cmt.exceptions import CmtError
from cmt.git.repository import Repository
from cmt.utils import edit_with_vim

app = typer.Typer()


@app.command()
def suggest() -> None:
    try:
        repository = Repository()
        analyzer = Analyzer()

        if not repository.is_git_repository():
            raise CmtError("Not a git repository.")

        staged_files = repository.get_staged_changes()
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
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=1) from None


@app.command()
def config(task: str) -> None:
    if task == "set":
        settings = Settings()

        open_ai_key = typer.prompt("Enter your OpenAI API key")
        open_ai_model = typer.prompt(
            "Enter your OpenAI model", default=settings.OPEN_AI_DEFAULT_MODEL
        )
        settings.set(OpenAIConfig(api_key=open_ai_key, model=open_ai_model))


if __name__ == "__main__":
    app()
