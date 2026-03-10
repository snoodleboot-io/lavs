import contextlib
from typing import Any


class Connection:
    """Abstraction for a data system connection."""

    def execute(self, query: str, **kwargs: Any) -> Any:
        """Execute a query."""
        raise NotImplementedError

    def fetchdf(self) -> Any:
        """Fetch results as DataFrame."""
        raise NotImplementedError

    @contextlib.contextmanager
    def connection(self) -> Any:  # type: ignore[reportGeneralTypeIssues]
        """Contextable method for retrieving a live data system connection."""
        raise NotImplementedError
