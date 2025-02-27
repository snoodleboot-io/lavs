from typing import Annotated

from fastapi import APIRouter, Query, Body

from app.models.requests.application_and_version_model import (
    ApplicationAndVersionNameModel,
)
from app.models.requests.application_name_model import ApplicationNameModel
from app.models.respones.applciation_and_version_response_model import (
    ApplicationAndVersionResponseModel,
)
from app.models.respones.response_model import ResponseModel
from app.queries.versions.create_version import CreateVersion
from app.queries.versions.delete_version import DeleteVersion
from app.queries.versions.retrieve_latest_version import RetrieveLatestVersion
from app.queries.versions.retrieve_version_history import RetrieveVersionHistory

router = APIRouter(tags=["versions"], prefix="/versions")


@router.get("/", response_model=ApplicationAndVersionResponseModel)
async def get(data: Annotated[ApplicationNameModel, Query()]):
    result = await RetrieveVersionHistory().execute(data=data)

    return result


@router.get("/latest", response_model=ApplicationAndVersionResponseModel)
async def get_all(data: Annotated[ApplicationNameModel, Query()]):
    result = await RetrieveLatestVersion().execute(data=data)

    return result


@router.post("/", response_model=ApplicationAndVersionResponseModel)
async def create(data: Annotated[ApplicationAndVersionNameModel, Query()]):
    result = await CreateVersion().execute(data=data)

    return result


@router.delete("/", response_model=ResponseModel)
async def read_all(data: Annotated[ApplicationAndVersionNameModel, Query()]):
    result = await DeleteVersion().execute(data=data)

    return result
