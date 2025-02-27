from typing import Any

from app.models.requests.application_and_version_model import (
    ApplicationAndVersionNameModel,
)
from app.models.respones.applciation_and_version_response_model import (
    ApplicationAndVersionResponseModel,
)
from app.models.respones.response_model import ResponseModel
from app.queries.query import Query
from app.queries.versions.retrieve_latest_version import RetrieveLatestVersion


class DeleteVersion(Query):
    """Delete a specific version."""

    def __init__(self):
        super().__init__()
        self._latest_version_query = RetrieveLatestVersion()

    async def apply(
        self, data: ApplicationAndVersionNameModel, conn: Any
    ) -> ApplicationAndVersionResponseModel | ResponseModel:
        """Delete a version from the database given the product name and its version.

        Args:
            data: Product name and version.
            conn: Live database connection.
        """
        _ = conn.sql(
            query=(
                f"DELETE FROM Versions "
                f"WHERE product_name='{data.product_name}' "
                f"AND major={data.major} "
                f"AND minor={data.minor} "
                f"AND patch={data.patch
                }"
            )
        )
        result: ApplicationAndVersionResponseModel = (
            await self._latest_version_query.execute(data=data)
        )

        self._logger.info(result)
        return result
