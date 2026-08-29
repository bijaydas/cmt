import typer

from cmt.ai.openai import OpenAIProvider
from cmt.analysis.analyzer import Analyzer
from cmt.config.settings import OpenAIConfig, Settings
from cmt.git.repository import Repository
from cmt.exceptions import CmtError

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
        typer.echo(commit)
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
            "Enter your OpenAI model",
            default=settings.OPEN_AI_DEFAULT_MODEL
        )
        settings.set(OpenAIConfig(api_key=open_ai_key, model=open_ai_model))

if __name__ == '__main__':
    app()
