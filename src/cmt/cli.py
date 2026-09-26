import logging
import sys
from importlib.metadata import version

import typer

from cmt.ai.openai import OpenAIProvider
from cmt.analysis.analyzer import Analyzer
from cmt.core import settings, setup_logging
from cmt.enums.config import ConfigTask
from cmt.exceptions import CmtError
from cmt.git.repository import Repository
from cmt.schemas.config import AIConfig
from cmt.services import PyPIService
from cmt.utils import edit_with_vim

logger = logging.getLogger(__name__)

app = typer.Typer(
    add_completion=False,
)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"cmt-cli version: {version(settings.APP_NAME)}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    flag: bool = typer.Option(False, "--version", callback=version_callback, is_eager=True),
) -> None:
    setup_logging()
    if ctx.invoked_subcommand is None:
        logger.info("No subcommand invoked, displaying help.")
        typer.echo(ctx.get_help())
        raise typer.Exit(code=0)


@app.command()
def suggest() -> None:
    """Suggest a commit message based on staged changes."""
    try:
        repository = Repository()
        analyzer = Analyzer()

        if not repository.is_git_repository():
            logger.error("Not a git repository.")
            raise CmtError("Not a git repository.")

        staged_files = repository.get_staged_changes()

        if not staged_files.files:
            logger.warning(
                "No staged files found. Please stage your changes before running this command."
            )
            typer.echo(
                "No staged files found. Please stage your changes before running this command."
            )
            raise typer.Exit(code=0)

        analysis_result = analyzer.analyze(staged_files)

        open_ai = OpenAIProvider()

        commit = open_ai.generate_commit_message(staged_files, analysis_result)
        sys.exit()
        commit_command = OpenAIProvider.commit_command(commit)

        logger.info("Suggested commit:\n\n%s", commit_command)
        typer.echo(f"Suggested commit:\n\n{commit_command}")

        while True:
            action = (
                typer.prompt("Use this message? [y]es / [e]dit / [n]o", default="y")
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
                logger.info("Committing with message:\n\n%s", commit_command)
                result = repository.commit(commit_command)

                logger.info("Commit result:\n\n%s", result.stdout)
                typer.echo(f"Commit result:\n\n{result.stdout}")
                break

    except CmtError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1) from None
    except typer.Exit:
        raise
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user.")
        typer.echo("\nOperation cancelled by user.", err=True)
        raise typer.Exit(code=1) from None
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=1) from None


@app.command()
def config(task: ConfigTask) -> None:
    """Configure cmt-cli configuration for OpenAI API key and model."""
    if task == ConfigTask.set:
        open_ai_key = typer.prompt("Enter your OpenAI API key", default=None)
        open_ai_model = typer.prompt(
            "Enter your OpenAI model", default=settings.OPEN_AI_DEFAULT_MODEL
        )
        logger.info("Configuration updated with OpenAI API key and model.")
        settings.set(AIConfig(api_key=open_ai_key, model=open_ai_model))

    if task == ConfigTask.get:
        setting_values = settings.get()

        if setting_values.api_key:
            typer.echo(f"OpenAI API key: {setting_values.api_key[:10]} ****")

        if setting_values.model:
            typer.echo(f"OpenAI model: {setting_values.model}")

        logger.info("Retrieved current configuration.")

        raise typer.Exit(code=0)


@app.command()
def update() -> None:
    """Update cmt-cli to the latest version."""
    logger.info("Starting update process for %s.", settings.APP_NAME)

    current_version = version(settings.APP_NAME)
    logger.info("Current %s version: %s", settings.APP_NAME, current_version)

    pypi_service = PyPIService()
    latest_info_response = pypi_service.any_update(current_version=current_version)

    if latest_info_response.updated_required:
        logger.info(
            "Update required: current version %s, latest version %s",
            latest_info_response.current_version,
            latest_info_response.latest_version,
        )
        typer.echo(
            f"A new version of {settings.APP_NAME} is available: "
            f"{latest_info_response.latest_version}.\n\n"
            f"upgrade {settings.APP_NAME} using your package manager.",
        )
    else:
        logger.info(
            "No update required. You are using the latest version: %s",
            latest_info_response.current_version,
        )
        typer.echo(f"You are using the latest version of {settings.APP_NAME}")

    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
