from typing import Any

from app.models.requests.application_name_model import ApplicationNameModel
from app.models.responses.application_and_version_response_model import (
    ApplicationAndVersionResponseModel,
)
from app.queries.query import Query


def _rows_to_dicts(description: list[tuple], rows: list[tuple]) -> list[dict]:
    """Convert query result rows to list of dictionaries.

    Args:
        description: Column descriptions from cursor.
        rows: Result rows from query execution.

    Returns:
        List of dictionaries representing the rows.
    """
    columns = [desc[0] for desc in description]
    return [dict(zip(columns, row, strict=False)) for row in rows]


class RetrieveVersionHistory(Query):
    """Retrive history of a products version."""

    def __init__(self):
        """Construct an instance of RetrieveVersionHistory."""
        super().__init__()

    async def apply(
        self, data: ApplicationNameModel, conn: Any
    ) -> list[ApplicationAndVersionResponseModel]:
        """Retrieve the entire version history for a given product.

        Args:
            data: Product name and version.
            conn: Live database connection.
        """
        query_result = conn.sql(
            "SELECT * FROM Versions WHERE product_name = ?", params=(data.product_name,)
        )
        result = _rows_to_dicts(query_result.description, query_result.fetchall())

        return [ApplicationAndVersionResponseModel(**row) for row in result]
