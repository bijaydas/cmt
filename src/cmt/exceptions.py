class CmtError(Exception):
    """Base exception for expected cmt errors."""


class ConfigurationError(CmtError):
    """Raised when cmt configuration is missing or invalid."""


class GitError(CmtError):
    """Raised when a Git operation fails."""


class AIError(CmtError):
    """Raised when AI processing fails."""