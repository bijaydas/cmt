from rich.console import Console as RichConsoleBase
from rich.panel import Panel
from rich.theme import Theme

CMT_THEME = Theme(
    {
        "brand": "bold magenta",
        "muted": "dim",
        "info": "cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "prompt.choices": "bold cyan",
    }
)


class RichConsole:
    def __init__(self) -> None:
        self._console = RichConsoleBase(theme=CMT_THEME, highlight=False)
        self._error_console = RichConsoleBase(theme=CMT_THEME, highlight=False, stderr=True)

    def get_console(self) -> RichConsoleBase:
        return self._console

    def get_error_console(self) -> RichConsoleBase:
        return self._error_console

    def print(self, *args, **kwargs) -> None:
        self._console.print(*args, **kwargs)

    def print_banner(self, app_name: str, version: str | None = None) -> None:
        label = f"[brand]✦ {app_name}[/brand]"
        if version:
            label += f" [muted]v{version}[/muted]"
        self._console.print(label)

    def print_success(self, message: str) -> None:
        self._console.print(f"[success]✔[/success] {message}")

    def print_warning(self, message: str) -> None:
        self._console.print(f"[warning]⚠[/warning] {message}")

    def print_info(self, message: str) -> None:
        self._console.print(f"[info]ℹ[/info] {message}")

    def print_error(self, message: str) -> None:
        self._error_console.print(f"[error]✖ {message}[/error]")

    def _render_commit_panel(self, commit_message: str, title: str = "Suggested commit") -> Panel:
        return Panel(
            commit_message,
            title=f"[brand]{title}[/brand]",
            title_align="left",
            border_style="brand",
            padding=(1, 2),
        )

    def render_summary_panel(self, summary: str, title: str = "Summary") -> Panel:
        return Panel(
            summary,
            title=f"[brand]{title}[/brand]",
            title_align="left",
            border_style="brand",
            padding=(1, 2),
        )

    def print_suggested_commit(self, commit_message: str, title: str = "Suggested commit") -> None:
        self._console.print(self._render_commit_panel(commit_message, title=title))

    def print_loading(self, message: str) -> None:
        self._console.status(f"[info]{message}[/info]", spinner="dots")


console = RichConsole()
