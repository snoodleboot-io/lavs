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


class RetrieveLatestVersion(Query):
    """Retrieve latest version of a product."""

    def __init__(self):
        """Construct an instance of RetrieveLatestVersion."""
        super().__init__()

    async def apply(
        self, data: ApplicationNameModel, conn: Any
    ) -> ApplicationAndVersionResponseModel | None:
        """Retrieve the latest version of a product.

        Args:
            data: Product name.
            conn: Live database connection.

        Returns:
            ApplicationAndVersionResponseModel if found, None otherwise.
        """
        query_result = conn.sql(
            "SELECT * FROM Versions WHERE product_name = ? ORDER BY major DESC, minor DESC, patch DESC LIMIT 1",
            params=(data.product_name,),
        )
        result = _rows_to_dicts(query_result.description, query_result.fetchall())
        if len(result) > 0:
            return ApplicationAndVersionResponseModel(**result[0])
        return None
