from unittest import IsolatedAsyncioTestCase

from app.database.database_manager import DatabaseManager
from app.models.requests.application_and_version_model import (
    ApplicationAndVersionNameModel,
)
from app.models.responses.application_and_version_response_model import (
    ApplicationAndVersionResponseModel,
)
from app.queries.versions.create_version import CreateVersion


class TestReadLatestVersion(IsolatedAsyncioTestCase):
    def setUp(self):
        DatabaseManager.create_tables()

    def tearDown(self):
        DatabaseManager.drop_tables()

    async def test_read_latest_version(self):
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
