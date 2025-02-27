from typing import Any

from app.models.requests.application_and_version_model import (
    ApplicationAndVersionNameModel,
)
from app.models.requests.request_model import RequestModel
from app.models.respones.applciation_and_version_response_model import (
    ApplicationAndVersionResponseModel,
)
from app.models.respones.response_model import ResponseModel
from app.queries.query import Query
from app.queries.versions.delete_version import DeleteVersion
from app.queries.versions.retrieve_latest_version import RetrieveLatestVersion


class RollbackToPreviousPatchVersion(Query):
    """Rollback active version the previous version."""

    def __init__(self):
        """Constructs an instance of RollbackToPreviousPatchVersion."""
        super().__init__()
        self._latest_version_query = RetrieveLatestVersion()
        self._delete_version_query = DeleteVersion()

    async def apply(
        self, data: ApplicationAndVersionNameModel, conn: Any
    ) -> ApplicationAndVersionResponseModel:
        """Roll back patch version by deleting the current version.

        Args:
            data: Product name and version.
            conn: Live database connection.
        """
        _ = await self._latest_version_query.execute(data=data)
        _ = await self._delete_version_query.execute(data=data)
        previous_version: ApplicationAndVersionResponseModel = (
            await self._latest_version_query.execute(data=data)
        )
        return previous_version
