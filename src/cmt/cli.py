import typer
from cmt.git.repository import Repository


app = typer.Typer()


@app.command()
def suggest() -> None:
    repository = Repository()

    if not repository.is_git_repository():
        typer.echo("Not a git repository.")
        raise typer.Exit(code=1)

    staged_files = repository.get_staged_files()

    if not staged_files:
        typer.echo("No staged files.")
        raise typer.Exit(code=0)

if __name__ == '__main__':
    app()