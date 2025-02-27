import re
from typing import Optional, Annotated

from annotated_types import Ge
from pydantic import field_validator, computed_field

from app.models.requests.request_model import RequestModel


class ApplicationAndVersionNameModel(RequestModel):
    """"""

    product_name: str
    version: Optional[str] = None

    @field_validator("version", mode="before")
    @classmethod
    def validate_version(cls, field_value: str) -> str:
        """This validation makes sure that the version string is a traditional semantic version.

        Args:
            field_value: value assigned to the version string.

        Raises:
            ValueError: When the version format is not valid.

        """
        rex = re.compile("[0-9]+\.[0-9]+\.[0-9]+")
        if rex.match(field_value):
            return field_value
        else:
            raise ValueError("version must be a semantic version number.")

    @computed_field
    @property
    def major(self) -> Annotated[int, Ge(0)]:
        """The major component of the semantic version."""
        return int(self.version.split(".")[0])

    @computed_field
    @property
    def minor(self) -> Annotated[int, Ge(0)]:
        """The minor component of the semantic version."""
        return int(self.version.split(".")[1])

    @computed_field
    @property
    def patch(self) -> Annotated[int, Ge(0)]:
        """The patch component of the semantic version."""
        return int(self.version.split(".")[2])

    model_config = {
        "json_schema_extra": {
            "examples": [{"product_name": "My Sample Product", "version": "1.2.3"}]
        }
    }
