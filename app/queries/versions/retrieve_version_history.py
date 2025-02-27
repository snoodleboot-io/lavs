from typing import Any, List

from app.models.requests.application_name_model import ApplicationNameModel
from app.models.requests.request_model import RequestModel
from app.models.respones.applciation_and_version_response_model import (
    ApplicationAndVersionResponseModel,
)
from app.models.respones.response_model import ResponseModel
from app.queries.query import Query


class RetrieveVersionHistory(Query):
    """Retrive history of a products version."""

    def __init__(self):
        """Construct an instance of RetrieveVersionHistory."""
        super().__init__()

    async def apply(
        self, data: ApplicationNameModel, conn: Any
    ) -> List[ApplicationAndVersionResponseModel]:
        """Retrieve the entire version history for a given product.

        Args:
            data: Product name and version.
            conn: Live database connection.
        """
        result: List[ApplicationAndVersionResponseModel] = (
            conn.sql(
                f"SELECT * FROM Versions WHERE product_name = '{data.product_name}'"
            )
            .fetchdf()
            .to_dict("records")
        )

        return result
