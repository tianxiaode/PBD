import unittest
from unittest.mock import patch, mock_open, MagicMock
import logging
from logging.handlers import RotatingFileHandler, QueueHandler
import os
from pydantic import ValidationError
import pytest
from pbd_core import Logger, LoggerSetting

OriginalStreamHandler = logging.StreamHandler
OriginalRotatingFileHandler = logging.handlers.RotatingFileHandler


class TestLogger(unittest.TestCase):

    def setUp(self):
        # 确保单例隔离
        Logger._instance = None
        # 清理root logger handler，防止测试间污染
        root_logger = logging.getLogger()
        for h in root_logger.handlers[:]:
            root_logger.removeHandler(h)
            h.close()

    def tearDown(self):
        self.setUp()

    @patch.dict(os.environ, {
        "LOG_FILE_PATH": "/mock/test.log",
        "LOG_TO_CONSOLE": "True",
        "LOG_USE_ASYNC": "False",
        "LOG_LEVEL": "DEBUG",
        "LOG_ENV": "production",
        "LOG_USE_JSON": "False",
        "LOG_IGNORE_MODULES": "ignoremod1,ignoremod2"
    })
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch.dict('sys.modules', {'rich.logging': None})  # rich 不可用
    def test_sync_logger_with_file_console_and_ignore_modules(self, mock_exists, mock_file_open):
        Logger.instance()
        root_logger = logging.getLogger()

        # 检查RotatingFileHandler和StreamHandler都被添加
        handlers = root_logger.handlers
        self.assertTrue(any(isinstance(h, RotatingFileHandler) for h in handlers), "RotatingFileHandler missing")
        self.assertTrue(any(isinstance(h, logging.StreamHandler) for h in handlers), "StreamHandler missing")

        # 检查ignore_modules是否生效
        ignore_logger1 = logging.getLogger("ignoremod1")
        ignore_logger2 = logging.getLogger("ignoremod2")
        self.assertFalse(ignore_logger1.propagate)
        self.assertFalse(ignore_logger2.propagate)

        # 检查文件open参数
        args, kwargs = mock_file_open.call_args
        self.assertEqual(args[1], 'a')
        self.assertEqual(kwargs.get('encoding'), 'utf-8')
        self.assertTrue(args[0].replace('\\', '/').endswith('/mock/test.log'))
        #mock_file_open.assert_called_with('/mock/test.log', 'a', encoding='utf-8')

        # 断言日志级别
        self.assertEqual(root_logger.level, logging.DEBUG)

    @patch.dict(os.environ, {
        "LOG_TO_CONSOLE": "True",
        "LOG_USE_ASYNC": "False",
        "LOG_ENV": "development",
        "LOG_USE_JSON": "False"
    })
    @patch.dict('sys.modules', {'rich': MagicMock()})  # 模拟rich.logging存在
    def test_console_handler_rich_handler(self):
        Logger.instance()
        root_logger = logging.getLogger()
        handlers = root_logger.handlers

        # 应该添加RichHandler（mock版）
        rich_handler_found = any('RichHandler' in h.__class__.__name__ for h in handlers)
        self.assertTrue(rich_handler_found, "RichHandler should be used in development env")

    @patch.dict(os.environ, {
        "LOG_FILE_PATH": "/mock/test.log",
        "LOG_TO_CONSOLE": "False",
        "LOG_USE_ASYNC": "True",
        "LOG_ENV": "production",
        "LOG_USE_JSON": "False"
    })
    @patch.dict('sys.modules', {'rich.logging': None})
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('logging.StreamHandler')
    @patch('logging.handlers.RotatingFileHandler')
    def test_async_logger_queue_handler(self,mock_rfh_cls, mock_stream_handler_cls, mock_exists, mock_file_open):
        # mock RotatingFileHandler 实例
        mock_stream_handler_instance = MagicMock(spec=OriginalStreamHandler)
        mock_stream_handler_cls.setFormatter = MagicMock()
        mock_stream_handler_cls.return_value = mock_stream_handler_instance

        mock_rfh_instance = MagicMock(spec=OriginalRotatingFileHandler)
        mock_rfh_instance.setFormatter = MagicMock()
        mock_rfh_cls.return_value = mock_rfh_instance
        
        # 重新实例化Logger，确保用mock
        Logger._instance = None
        Logger.instance()
        root_logger = logging.getLogger()
        
        # 确认有 QueueHandler
        queue_handler_found = any(isinstance(h, QueueHandler) for h in root_logger.handlers)
        assert queue_handler_found, "QueueHandler missing in async mode"

    @patch.dict(os.environ, {
        "LOG_FILE_PATH": "/mock/test.log",
        "LOG_TO_CONSOLE": "True",
        "LOG_USE_ASYNC": "False",
        "LOG_USE_JSON": "True",
        "LOG_ENV": "production"
    })
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_json_formatter_fallback(self, mock_exists, mock_file_open):
        # 这里模拟导入json_formatter失败，走except分支
        with patch('logging_utilities.formatters.json_formatter.JsonFormatter', side_effect=ImportError):
            Logger.instance()
            root_logger = logging.getLogger()
            # 只要能初始化成功即可，具体formatter的测试可另写

    def test_singleton_instance(self):
        # 多次调用 instance 返回同一对象
        inst1 = Logger.instance()
        inst2 = Logger.instance()
        self.assertIs(inst1, inst2, "Logger.instance() should return singleton")

    def test_get_class_logger_name(self):
        class Dummy:
            __module__ = 'a.b.c'
            __name__ = 'DummyClass'

        name = Logger.get_class_logger_name(Dummy)
        self.assertEqual(name, 'b.c.Dummy')

        class DummyGroup:
            __module__ = 'x.y.z'
            __name__ = 'DummyGroup'
            __module_group__ = 'custom.group'

        name2 = Logger.get_class_logger_name(DummyGroup)
        self.assertEqual(name2, 'custom.group.DummyGroup')

    @patch('logging.handlers.RotatingFileHandler.__init__', return_value=None)
    def test_configure_handler_sets_formatter(self, mock_init):
        Logger._instance = None
        Logger.instance()
        rh = RotatingFileHandler('/mock/test.log')  # 这时不执行真实初始化
        # 需要手动给 formatter 属性赋值，因为 __init__ 被跳过了
        rh.formatter = None
        handler = Logger._instance._configure_handler(rh)
        self.assertIs(handler.formatter, rh.formatter)

    def test_get_formatter_json_and_plain(self):
        # plain formatter
        Logger._instance = None
        with patch.dict(os.environ, {"LOG_USE_JSON": "False"}):
            Logger.instance()
            formatter = Logger._instance._get_formatter()
            self.assertIsInstance(formatter, logging.Formatter)

        # json formatter - 模拟成功导入json_formatter
        Logger._instance = None
        mock_json_formatter_cls = MagicMock()
        with patch.dict(os.environ, {"LOG_USE_JSON": "True"}):
            with patch('logging_utilities.formatters.json_formatter.JsonFormatter', mock_json_formatter_cls):
                Logger.instance()
                formatter = Logger._instance._get_formatter()
                self.assertEqual(formatter, mock_json_formatter_cls())

    @patch.dict(os.environ, {"LOG_USE_ASYNC": "False"})
    def test_async_handler_returns_none_when_disabled(self):
        handler = Logger.instance()._get_queue_handler()
        self.assertIsNone(handler)                

    @patch('logging.Logger.error')
    def test_cleanup_listener_with_exception(self, mock_error):
        mock_listener = MagicMock()
        mock_exception = Exception("Mock error")
        mock_listener.stop.side_effect = mock_exception
        Logger.instance()._cleanup_listener(mock_listener)
        mock_error.assert_called_with("监听清理失败: %s", mock_exception) 

    def test_initialize_settings_skips_fields_without_env(self):
        with patch.object(LoggerSetting, 'model_fields', {
            "no_env_field": MagicMock(json_schema_extra={})  # 无 env 配置
        }):
            Logger._instance = None
            Logger.instance()  # 应跳过 no_env_field
            self.assertNotIn("no_env_field", Logger._instance._settings.model_dump())

    @patch.dict(os.environ, {"LOG_IGNORE_MODULES": ""})  # 空列表
    def test_ignore_modules_with_empty_list(self):
        self.assertIsNone(Logger.instance()._ignore_modules(None))

    def test_get_logger_with_different_name_types(self):
        # 测试 name=None
        logger_none = Logger.get_logger()
        self.assertEqual(logger_none.name, "app")

        # 测试 name 为字符串
        logger_str = Logger.get_logger("test")
        self.assertEqual(logger_str.name, "test")

        # 测试 name 为类
        class TestClass:
            __module__ = "module"
        logger_class = Logger.get_logger(TestClass)
        self.assertEqual(logger_class.name, "module.TestClass")

    def test_int_field_parsing_from_env(self):
        with patch.dict(os.environ, {"LOG_MAX_SIZE":"2048"}, clear=True):
            Logger.instance()._initialize_settings()            
            assert Logger._instance._settings.max_size == 2048

    def test_int_field_parsing_invalid_from_env(self):
        with patch.dict(os.environ, {"LOG_MAX_SIZE":"invalid"}, clear=True):
            with pytest.raises(ValidationError) as excinfo:
                Logger.instance()._initialize_settings()   
            errors = excinfo.value.errors()
            assert len(errors) == 1, "Expected exactly one validation error"
            assert errors[0]['loc'] == ('max_size',), "Error location should be 'max_size'"
            assert "should be a valid integer" in errors[0]['msg']

       
    @patch.dict(os.environ, {"LOG_TO_CONSOLE": "1"})  # 测试 '1' 转换为 True
    def test_bool_field_parsing_true_1(self):
        Logger._instance = None
        Logger.instance()
        self.assertTrue(Logger._instance._settings.log_to_console)

    @patch.dict(os.environ, {"LOG_TO_CONSOLE": "t"})  # 测试 't' 转换为 True
    def test_bool_field_parsing_true_t(self):
        Logger._instance = None
        Logger.instance()
        self.assertTrue(Logger._instance._settings.log_to_console)

    @patch.dict(os.environ, {"LOG_TO_CONSOLE": "false"})  # 测试假值
    def test_bool_field_parsing_false(self):
        Logger._instance = None
        Logger.instance()
        self.assertFalse(Logger._instance._settings.log_to_console)        

if __name__ == "__main__":
    unittest.main()
