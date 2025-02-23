import traceback
import typing
from logging import getLogger
from typing import Any

from app.configurations.configuration import Configuration
from app.connections.connection_factory import ConnectionFactory
from app.models.requests.request_model import RequestModel
from app.models.respones.applciation_and_version_response_model import (
    ApplicationAndVersionResponseModel,
)
from app.models.respones.patch_response_model import PatchResponseModel


T = typing.TypeVar(
    "T",
    ApplicationAndVersionResponseModel,
    PatchResponseModel,
    typing.List[ApplicationAndVersionResponseModel],
)


class Query:
    def __init__(self):
        self._logger = getLogger(Configuration().application_name)

    async def execute(self, data: RequestModel) -> T:
        try:
            with ConnectionFactory().retrieve(key="duckdb") as conn:
                result = await self.apply(data, conn)
        except:
            self._logger.error(traceback.format_exc())
            raise

        return result

    async def apply(self, data: RequestModel, conn: Any) -> T:
        raise NotImplementedError
