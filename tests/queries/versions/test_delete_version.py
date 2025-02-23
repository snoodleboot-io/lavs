from unittest import IsolatedAsyncioTestCase

from app.database.database_manager import DatabaseManager
from app.models.requests.application_and_version_model import (
    ApplicationAndVersionNameModel,
)
from app.models.respones.applciation_and_version_response_model import (
    ApplicationAndVersionResponseModel,
)
from app.models.respones.response_model import ResponseModel
from app.queries.versions.create_version import CreateVersion
from app.queries.versions.delete_version import DeleteVersion
from app.queries.versions.retrieve_latest_version import RetrieveLatestVersion


class TestDeleteVersion(IsolatedAsyncioTestCase):
    def setUp(self):
        DatabaseManager.create_tables()

    def tearDown(self):
        DatabaseManager.drop_tables()

    async def test_create_version(self):
        data = ApplicationAndVersionNameModel(product_name="test", version="1.1.1")
        expected_result = ApplicationAndVersionResponseModel(
            **{
                "major": 1,
                "minor": 1,
                "patch": 1,
                "product_name": "test",
                "id": 1,
            }
        )
        result = await CreateVersion().execute(data=data)
        self.assertTrue(result == expected_result)
        await DeleteVersion().execute(data=data)
        result = await RetrieveLatestVersion().execute(data=data)
        self.assertIsInstance(result, ResponseModel)
        self.assertTrue(result == ResponseModel())
