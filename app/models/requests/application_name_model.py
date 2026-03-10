from app.models.requests.request_model import RequestModel


class ApplicationNameModel(RequestModel):
    product_name: str

    model_config = {"json_schema_extra": {"examples": [{"product_name": "My Sample Product"}]}}
