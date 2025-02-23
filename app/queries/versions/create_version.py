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


class CreateVersion(Query):
    """Create a new version entry."""

    def __init__(self):
        """Constructs an instance of CreateVersion."""
        super().__init__()
        self._latest_version_query = RetrieveLatestVersion()

    async def apply(
        self, data: ApplicationAndVersionNameModel, conn: Any
    ) -> ApplicationAndVersionResponseModel:
        """Create a new version entry given the product name and the version.

        Args:
            data: Product name and version.
            conn: Live database connection.
        """
        _ = conn.sql(
            query=(
                f"INSERT INTO Versions "
                f"(major, minor, patch, product_name, id) "
                f"VALUES ({data.major}, {data.minor}, {data.patch}, '{data.product_name}', nextval('version_id_seq'))"
            )
        )
        result: ApplicationAndVersionResponseModel = (
            await self._latest_version_query.execute(data=data)
        )
        self._logger.info(result)
        return result
