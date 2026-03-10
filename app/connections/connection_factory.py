import contextlib
from collections.abc import Generator

from app.connections.connection import Connection
from app.connections.duckdb_connection import DuckDBConnection


class ConnectionFactory:
    __registry = {"duckdb": DuckDBConnection}

    @contextlib.contextmanager
    def retrieve(self, key: str) -> Generator[Connection]:
        """Will find and retrieve a Connection object - not an instance.

        Args:
            key: identifier for the Connection to return.

        Raises:
            ValueError: When the key is not a valid key.
        """
        if self.__registry.get(key):
            with self.__registry[key]().connection as conn:  # type: ignore[reportGeneralTypeIssues]
                yield conn
        else:
            raise ValueError
