from typing import Annotated

from annotated_types import Ge
from pydantic import computed_field

from app.models.respones.response_model import ResponseModel


class ApplicationAndVersionResponseModel(ResponseModel):
    """"""

    product_name: str
    major: Annotated[int, Ge(0)]
    minor: Annotated[int, Ge(0)]
    patch: Annotated[int, Ge(0)]
    id: Annotated[int, Ge(0)]

    @computed_field
    @property
    def version(self) -> str:
        """The major component of the semantic version."""
        return f"{self.major}.{self.minor}.{self.patch}"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "product_name": "My Sample Product",
                    "version": "1.2.3",
                    "major": 1,
                    "minor": 2,
                    "patch": 3,
                }
            ]
        }
    }
