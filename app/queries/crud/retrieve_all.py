from typing import Any, List

from app.models.requests.request_model import RequestModel
from app.models.respones.applciation_and_version_response_model import (
    ApplicationAndVersionResponseModel,
)
from app.models.respones.response_model import ResponseModel
from app.queries.query import Query


class RetrieveAll(Query):
    """Query to retrieve all versions."""

    def __init__(self):
        """Construct and instance of RetrieveAll."""
        super().__init__()

    async def apply(
        self, data: RequestModel, conn: Any
    ) -> List[ApplicationAndVersionResponseModel]:
        """Queries all versions of all products.

        Args:
            data: Empty RequestModel.
            conn: Live database connection.
        """
        result = (
            conn.sql(
                f"SELECT * FROM Versions WHERE ORDER BY major DESC, minor DESC, patch DESC"
            )
            .fetchdf()
            .to_dict("records")
        )
        self._logger.info(result)
        return result
