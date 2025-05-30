import unittest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from pbd_di.scoped_context import ScopedContext


class TestScopedContext(unittest.IsolatedAsyncioTestCase):
    async def test_happy_path(self):
        scoped_context = ScopedContext()
        async with scoped_context.scope():
            scoped_context.set("test_key", "test_value")
            self.assertEqual(scoped_context.get("test_key"), "test_value")
        self.assertIsNone(scoped_context.get("test_key"))

    async def test_edge_case_no_instances(self):
        scoped_context = ScopedContext()
        async with scoped_context.scope():
            pass
        self.assertEqual(scoped_context.get("non_existent_key"), None)

    async def test_edge_case_instance_without_close(self):
        scoped_context = ScopedContext()
        async with scoped_context.scope():
            scoped_context.set("test_key", MagicMock())
            self.assertEqual(scoped_context.get("test_key"), scoped_context._context.get()["test_key"])
        self.assertIsNone(scoped_context.get("test_key"))

    async def test_edge_case_instance_with_sync_close(self):
        scoped_context = ScopedContext()
        mock_instance = MagicMock()
        mock_instance.close = MagicMock()
        async with scoped_context.scope():
            scoped_context.set("test_key", mock_instance)
        mock_instance.close.assert_called_once()

    async def test_edge_case_instance_with_async_close(self):
        scoped_context = ScopedContext()
        mock_instance = MagicMock()
        mock_instance.close = AsyncMock()
        async with scoped_context.scope():
            scoped_context.set("test_key", mock_instance)
        mock_instance.close.assert_awaited_once()

    async def test_edge_case_multiple_instances(self):
        scoped_context = ScopedContext()
        mock_instance1 = MagicMock()
        mock_instance1.close = AsyncMock()
        mock_instance2 = MagicMock()
        mock_instance2.close = MagicMock()
        async with scoped_context.scope():
            scoped_context.set("test_key1", mock_instance1)
            scoped_context.set("test_key2", mock_instance2)
        mock_instance1.close.assert_awaited_once()
        mock_instance2.close.assert_called_once()

    async def test_edge_case_exception_in_scope(self):
        scoped_context = ScopedContext()
        mock_instance = MagicMock()
        mock_instance.close = AsyncMock()
        
        with self.assertRaises(Exception):  # 使用同步的 assertRaises
            async with scoped_context.scope():
                scoped_context.set("test_key", mock_instance)
                raise Exception("Test exception")
        
        mock_instance.close.assert_awaited_once()  # 修复断言方法

    async def test_edge_case_nested_scopes(self):
        scoped_context = ScopedContext()
        mock_instance1 = MagicMock()
        mock_instance1.close = AsyncMock()
        mock_instance2 = MagicMock()
        mock_instance2.close = MagicMock()
        async with scoped_context.scope():
            scoped_context.set("test_key1", mock_instance1)
            async with scoped_context.scope():
                scoped_context.set("test_key2", mock_instance2)
                self.assertIsNone(scoped_context.get("test_key1"))
        mock_instance1.close.assert_awaited_once()
        mock_instance2.close.assert_called_once()