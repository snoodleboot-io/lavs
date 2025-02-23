from typing import Annotated

from annotated_types import Ge
from pydantic import BaseModel


class PatchResponseModel(BaseModel):
    product_name: str
    patch: Annotated[int, Ge(0)]
    id: Annotated[int, Ge(0)]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "product_name": "My Sample Product",
                    "patch": 3,
                }
            ]
        }
    }
