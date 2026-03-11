import traceback
import typing
from logging import getLogger
from typing import Any, Generic

from app.configurations.configuration import Configuration
from app.connections.connection_factory import ConnectionFactory
from app.models.requests.request_model import RequestModel
from app.models.responses.application_and_version_response_model import (
    ApplicationAndVersionResponseModel,
)
from app.models.responses.patch_response_model import PatchResponseModel

T = typing.TypeVar(
    "T",
    ApplicationAndVersionResponseModel,
    PatchResponseModel,
    list[ApplicationAndVersionResponseModel],
)


class Query(Generic[T]):
    def __init__(self):
        self._logger = getLogger(Configuration().application_name)

    async def execute(self, data: RequestModel) -> T:
        try:
            with ConnectionFactory().retrieve(key="duckdb") as conn:
                result = await self.apply(data, conn)  # type: ignore[arg-type]
        except:
            self._logger.error(traceback.format_exc())
            raise

        return result

    async def apply(self, data: Any, conn: Any) -> T:
        raise NotImplementedError
