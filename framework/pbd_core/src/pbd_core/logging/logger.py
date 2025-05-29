import atexit
import logging
import os
import sys
import queue  # 标准库的Queue
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from queue import Queue
from typing import List, Optional, Union
from .logger_setting import LoggerSetting

logger = logging.getLogger(__name__)

class Logger:
    _instance = None
    _log_queue: Optional[Queue] = None
    def __init__(self):
        self._initialize_settings()
        self._initialize_logger()
 
    @staticmethod
    def instance() -> "Logger":
        if Logger._instance is None:
            Logger._instance = Logger()
        return Logger._instance

    @staticmethod
    def get_logger( name: Union[str, type, None] = None) -> logging.Logger:
        Logger.instance()
        if isinstance(name, type):
            name = Logger.get_class_logger_name(name)
        elif name is None:
            name = "app"
        return logging.getLogger(name)

    @staticmethod
    def get_class_logger_name(cls: type) -> str:
        """获取类对应的日志器名称"""
        if hasattr(cls, "__module_group__"):
            group = cls.__module_group__
        else:
            module_parts = cls.__module__.split('.')
            group = '.'.join(module_parts[-2:]) if len(module_parts)>=2 else module_parts[-1]
        return f"{group}.{cls.__name__}"

    def _initialize_logger(self):
        """初始化日志配置。"""
        settings = self._settings

        root_logger = logging.getLogger()
        root_logger.setLevel(settings.level.upper())
        


        # 添加处理器
        self._reconfigure_handlers(root_logger)
        
        # 忽略指定模块的日志输出
        self._ignore_modules(settings.ignore_modules)


    def _reconfigure_handlers(self, root_logger: logging.Logger):
        """重构处理器"""

        # 清空所有处理器
        for handler in root_logger.handlers[:]:
            handler.close()
            root_logger.removeHandler(handler)

        handlers: List[logging.Handler] = []
        if not self._settings.use_async:
            # 同步模式下直接添加文件和控制台处理器
            file_handler = self._get_file_handler()
            console_handler = self._get_console_handler()
            handlers.extend([file_handler, console_handler])
        else:
            # 异步模式下只添加队列处理器
            queue_handler = self._get_queue_handler()
            handlers.append(queue_handler)

        for handler in handlers:
            if handler : 
                root_logger.addHandler(handler)
    
    def _get_file_handler(self)-> Optional[logging.Handler]:
        if self._settings.file_path is None:
            return None
        
        handler = RotatingFileHandler(
            filename=self._settings.file_path,
            maxBytes=self._settings.max_size,
            backupCount=self._settings.backups,
            encoding='utf-8'
        ) 
        return self._configure_handler(handler)
    
    def _get_console_handler(self)-> Optional[logging.Handler]:
        handler = None
        if self._settings.env == 'development':
            try:
                from rich.logging import RichHandler
                handler = RichHandler(show_path=False, rich_tracebacks=True)
            except ImportError:
                pass

        if handler is None and self._settings.log_to_console is True:
            handler = logging.StreamHandler(sys.stdout)
        return self._configure_handler(handler)


    def _get_queue_handler(self) -> Optional[logging.Handler]:
        """获取异步队列处理器"""
        if not self._settings.use_async:
            return None

        self._log_queue = queue.Queue(-1)
        queue_handler = QueueHandler(self._log_queue)

        # 监听器应使用独立的处理器（避免复用根日志记录器的处理器）
        file_handler = self._get_file_handler()
        console_handler = self._get_console_handler()
        # 必须清空formatter，否则日志会被格式化两次
        if hasattr(console_handler, 'setFormatter'):
            console_handler.setFormatter(None)
        handlers = [h for h in [file_handler, console_handler] if h]

        listener = self._create_queue_listener(self._log_queue, handlers)
        listener.start()
        atexit.register(self._cleanup_listener, listener)

        return queue_handler


    def _create_queue_listener(self, log_queue, handlers):
        return QueueListener(log_queue, *handlers)

    def _cleanup_listener(self, listener):
        try:
            listener.stop()
        except Exception as e:
            logger.error("监听清理失败: %s", e)

    
    def _initialize_settings(self):
        """根据LogSettings从环境变量获取日志"""
        # 获取LoggerSetting模型的字段信息
        settings_fields = LoggerSetting.model_fields
        
        # 构建参数字典
        kwargs = {}
        for field_name, field_info in settings_fields.items():
            # 获取字段的env配置（可能是字符串或列表）
            env_var = field_info.json_schema_extra.get('env')
            if not env_var:
                continue
                
            
            # 尝试从环境变量获取值
            env_val = None
            env_val = os.getenv(env_var)
            if env_val is not None:
                # 根据字段类型转换值
                field_type = field_info.annotation
                if isinstance(field_type, bool):
                    kwargs[field_name] = env_val.lower() in ('true', '1', 't')
                elif isinstance(field_type, int):
                    kwargs[field_name] = int(env_val)
                elif field_type == list[str]:
                    kwargs[field_name] = env_val.split(',')
                else:
                    kwargs[field_name] = env_val 
        self._settings = LoggerSetting(**kwargs)   
            
    def _configure_handler(self, handler: logging.Handler):
        """配置处理器"""
        if hasattr(handler, 'setFormatter'):
            handler.setFormatter(self._get_formatter())
        return handler
    
    def _get_formatter(self):
        settings: LoggerSetting = self._settings
        formatter = logging.Formatter(
            fmt=settings.format,
            datefmt=settings.date_format
        )
        if settings.use_json:
            try:
                # 需要 pip install logging-utilities
                from logging_utilities.formatters.json_formatter import JsonFormatter
                formatter = JsonFormatter()
            except ImportError:
                pass
        return formatter



    def _ignore_modules(self, modules: List[str]):
        """忽略模块日志"""
        if not modules: 
            return
        for module in modules:
            logging.getLogger(module).propagate = False        

