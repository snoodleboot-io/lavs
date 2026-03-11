from typing import Any

from app.models.requests.application_and_version_model import (
    ApplicationAndVersionNameModel,
)
from app.models.responses.application_and_version_response_model import (
    ApplicationAndVersionResponseModel,
)
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
        # First get the current latest version
        current_version = await self._latest_version_query.execute(data=data)

        if current_version is None:
            raise ValueError(
                f"No version found for product '{data.product_name}'. " "Cannot rollback."
            )

        # Create version info to delete the current version
        version_to_delete = ApplicationAndVersionNameModel(
            product_name=current_version.product_name,
            version=f"{current_version.major}.{current_version.minor}.{current_version.patch}",
        )

        # Delete the current version
        await self._delete_version_query.execute(data=version_to_delete)

        # Get the previous version (now the latest)
        previous_version = await self._latest_version_query.execute(data=data)

        if previous_version is None:
            raise ValueError(
                f"No previous version found for product '{data.product_name}'. "
                "Cannot rollback to previous version."
            )

        return previous_version
