from typing import Any

from app.models.requests.application_name_model import ApplicationNameModel
from app.models.respones.applciation_and_version_response_model import (
    ApplicationAndVersionResponseModel,
)
from app.models.respones.response_model import ResponseModel
from app.queries.query import Query


class RetrieveLatestVersion(Query):
    """Retrieve latest version of a product."""

    def __init__(self):
        """Construct an instance of RetrieveLatestVersion."""
        super().__init__()

    async def apply(
        self, data: ApplicationNameModel, conn: Any
    ) -> ApplicationAndVersionResponseModel | ResponseModel:
        """Retrieve the latest version of a product.

        Args:
            data: Product name.
            conn: Live database connection.

        Returns:

        """
        result = (
            conn.sql(
                f"SELECT * FROM Versions WHERE product_name = '{data.product_name}' ORDER BY major DESC, minor DESC, patch DESC LIMIT 1"
            )
            .fetchdf()
            .to_dict("records")
        )
        if len(result) > 0:
            return ApplicationAndVersionResponseModel(**result[0])
        else:
            return ResponseModel()
