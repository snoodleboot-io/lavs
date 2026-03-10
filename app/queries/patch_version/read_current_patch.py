from typing import Any

from app.models.requests.application_name_model import ApplicationNameModel
from app.models.respones.patch_response_model import PatchResponseModel
from app.queries.query import Query
from app.queries.versions.retrieve_latest_version import RetrieveLatestVersion


class ReadCurrentPatch(Query):
    """Read the patch for a specific product."""

    def __init__(self):
        """Constructs an instnace of ReadCurrentPatch."""
        super().__init__()
        self._latest_version_query = RetrieveLatestVersion()

    async def apply(self, data: ApplicationNameModel, conn: Any) -> PatchResponseModel:
        """Read the current patch for a given product.

        Args:
            data: Product name.
            conn: Live database connection.
        """
        latest_version_result: PatchResponseModel = await self._latest_version_query.execute(
            data=data
        )
        return latest_version_result
