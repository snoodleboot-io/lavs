import os

from app.connections.connection_factory import ConnectionFactory


class DatabaseManager:
    """Manage the life-cycle of the database."""

    @classmethod
    def create_tables(cls):
        """Create the tables for the database."""

        with ConnectionFactory().retrieve(key="duckdb") as conn:
            with open(os.path.join(os.path.dirname(__file__), "duckdb/ddl.sql")) as stream:
                query = "".join(stream.readlines())

            conn.execute(query=query)

            result = conn.execute("SELECT COUNT(*) as COUNT FROM Versions").fetchall()
            _ = result  # Verify query executes without error

            table_result = conn.execute("SHOW ALL TABLES").fetchall()
            # Description: [('database',), ('schema',), ('name',), ...]
            # So name is at index 2
            table_names = [row[2] for row in table_result]
            assert "Versions" in table_names

    @classmethod
    def drop_tables(cls):
        """Drop all tables."""
        with ConnectionFactory().retrieve(key="duckdb") as conn:
            table_result = conn.execute("SHOW ALL TABLES").fetchall()
            # Description: [('database',), ('schema',), ('name',), ...]
            # So name is at index 2
            table_names = [row[2] for row in table_result]
            if "Versions" in table_names:
                conn.execute(query="DROP TABLE Versions")

            conn.execute(query="DROP SEQUENCE IF EXISTS version_id_seq")

            table_result = conn.execute("SHOW ALL TABLES").fetchall()
            table_names = [row[2] for row in table_result]
            assert "Versions" not in table_names
