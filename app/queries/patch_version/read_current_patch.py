from typing import Any

from app.models.requests.application_name_model import ApplicationNameModel
from app.models.responses.patch_response_model import PatchResponseModel
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
        latest_version_result = await self._latest_version_query.execute(data=data)
        if latest_version_result is None:
            raise ValueError(
                f"No version found for product '{data.product_name}'. "
                "Create a base version first using POST /versions/"
            )
        return PatchResponseModel(
            product_name=latest_version_result.product_name,
            patch=latest_version_result.patch,
            id=latest_version_result.id,
        )
