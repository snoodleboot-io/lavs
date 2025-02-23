from typing import Annotated

from fastapi import APIRouter, Query

from app.models.requests.application_name_model import ApplicationNameModel
from app.queries.patch_version.create_patch import CreatePatch
from app.queries.patch_version.read_current_patch import ReadCurrentPatch
from app.queries.patch_version.rollback_to_previous_patch_version import (
    RollbackToPreviousPatchVersion,
)

router = APIRouter(tags=["patch"], prefix="/patch")


@router.post("/")
async def create(data: Annotated[ApplicationNameModel, Query()]):
    """Create the next patch version."""
    result = await CreatePatch().execute(data=data)

    return {"result": result}


@router.get("/")
async def get(data: Annotated[ApplicationNameModel, Query()]):
    """Retrieve the next patch version."""
    result = await ReadCurrentPatch().execute(data=data)

    return {"result": result}


@router.post("/rollback")
async def rollback(data: Annotated[ApplicationNameModel, Query()]):
    result = await RollbackToPreviousPatchVersion().execute(data=data)

    return {"result": result}
