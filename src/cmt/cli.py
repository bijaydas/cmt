import logging
from importlib.metadata import version

import typer

from cmt.commands.suggest import SuggestCommand
from cmt.commands.summary import SummaryCommand
from cmt.core import (
    console,
    settings,
    setup_logging,
)
from cmt.enums.config import ConfigTask
from cmt.exceptions import CmtError
from cmt.schemas.config import AIConfig
from cmt.services import PyPIService

logger = logging.getLogger(__name__)

app = typer.Typer(
    add_completion=False,
)


def version_callback(value: bool) -> None:
    if value:
        console.print(f"[brand]cmt-cli[/brand] [muted]version {version(settings.APP_NAME)}[/muted]")
        console.print("Run 'cmt update' to check for updates.")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    flag: bool = typer.Option(False, "--version", callback=version_callback, is_eager=True),
) -> None:
    setup_logging()
    if ctx.invoked_subcommand is None:
        logger.info("No subcommand invoked, displaying help.")
        console.print(ctx.get_help())
        raise typer.Exit(code=0)


@app.command()
def suggest() -> None:
    """Suggest a commit message based on staged changes."""
    try:
        SuggestCommand().run()
    except CmtError as e:
        console.print_error(str(e))
        logger.error("CmtError: %s", e)
        raise typer.Exit(code=1) from None
    except typer.Exit:
        raise
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user.")
        console.print_warning("Operation cancelled by user.")
        raise typer.Exit(code=1) from None
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        console.print_error(f"\nUnexpected error: {e}")
        raise typer.Exit(code=1) from None


@app.command()
def config(task: ConfigTask) -> None:
    """Configure cmt-cli configuration for OpenAI API key and model."""
    if task == ConfigTask.set:
        open_ai_key = typer.prompt("Enter your OpenAI API key", default=None)
        open_ai_model = typer.prompt(
            "Enter your OpenAI model",
            default=settings.OPEN_AI_DEFAULT_MODEL,
        )
        logger.info("Configuration updated with OpenAI API key and model.")
        settings.set(AIConfig(api_key=open_ai_key, model=open_ai_model))

        console.print_success("Configuration updated.")

    if task == ConfigTask.get:
        setting_values = settings.get()

        if setting_values.api_key:
            typer.echo(f"OpenAI API key: {setting_values.api_key[:10]} ****")

        if setting_values.model:
            typer.echo(f"OpenAI model: {setting_values.model}")

        typer.echo("Run `cmt config set` to update the configuration.")

        logger.info("Retrieved current configuration.")

        raise typer.Exit(code=0)


@app.command()
def update() -> None:
    """Update cmt-cli to the latest version."""
    logger.info("Starting update process for %s.", settings.APP_NAME)

    current_version = version(settings.APP_NAME)
    logger.info("Current %s version: %s", settings.APP_NAME, current_version)

    with console.get_console().status("[brand]Checking for updates...[/brand]", spinner="dots"):
        pypi_service = PyPIService()
        latest_info_response = pypi_service.any_update(current_version=current_version)

    if latest_info_response.updated_required:
        logger.info(
            "Update required: current version %s, latest version %s",
            latest_info_response.current_version,
            latest_info_response.latest_version,
        )
        console.print(
            f"A new version of {settings.APP_NAME} is available: "
            f"[brand]{latest_info_response.latest_version}[/brand].\n\n"
            f"upgrade {settings.APP_NAME} using your package manager."
        )
    else:
        logger.info(
            "No update required. You are using the latest version: %s",
            latest_info_response.current_version,
        )
        console.print_success(
            f"You are using the latest version {latest_info_response.current_version}"
        )

    raise typer.Exit(code=0)


@app.command()
def summary() -> None:
    """Generate a summary of the current Git repository"""
    try:
        SummaryCommand().run()
    except CmtError as e:
        console.print_error(str(e))
        logger.error("CmtError: %s", e)
        raise typer.Exit(code=1) from None
    except Exception as e:
        raise e


if __name__ == "__main__":
    app()
