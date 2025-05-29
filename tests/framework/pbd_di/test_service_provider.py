import unittest
from unittest.mock import AsyncMock, patch
from typing import Type
from pbd_di import ServiceProvider

class TestServiceProvider(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.service_provider = ServiceProvider()

    async def test_get_service_happy_path(self):
        with patch('pbd_di.service_provider.Container') as mock_container:
            mock_container_instance = AsyncMock()
            mock_container.return_value = mock_container_instance
            expected_service = "Expected Service"
            mock_container_instance.get.return_value = expected_service

            service_type = Type[int]
            result = await self.service_provider.get(service_type)

            self.assertEqual(result, expected_service)
            mock_container_instance.get.assert_awaited_once_with(service_type)

    async def test_get_service_with_none_service_type(self):
        with patch('pbd_di.service_provider.Container') as mock_container:
            mock_container_instance = AsyncMock()
            mock_container.return_value = mock_container_instance
            mock_container_instance.get.side_effect = ValueError("Service type cannot be None")

            with self.assertRaises(ValueError) as context:
                await self.service_provider.get(None)

            self.assertTrue("Service type cannot be None" in str(context.exception))

    async def test_get_service_not_found(self):
        with patch('pbd_di.service_provider.Container') as mock_container:
            mock_container_instance = AsyncMock()
            mock_container.return_value = mock_container_instance
            mock_container_instance.get.side_effect = KeyError("Service not found")

            with self.assertRaises(KeyError) as context:
                await self.service_provider.get(Type[int])

            self.assertTrue("Service not found" in str(context.exception))

    async def test_get_service_with_invalid_service_type(self):
        with patch('pbd_di.service_provider.Container') as mock_container:
            mock_container_instance = AsyncMock()
            mock_container.return_value = mock_container_instance
            mock_container_instance.get.side_effect = TypeError("Invalid service type")

            with self.assertRaises(TypeError) as context:
                await self.service_provider.get("Invalid Type")

            self.assertTrue("Invalid service type" in str(context.exception))

