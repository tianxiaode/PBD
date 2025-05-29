from typing import Optional
from pydantic import BaseModel, Field

class LoggerSetting(BaseModel):
    env: str = Field(default="development", json_schema_extra={"env": "ENVIRONMENT"})
    level: str = Field(default="INFO", json_schema_extra={"env": "LOG_LEVEL"})
    format: str = Field(default="%(asctime)s %(levelname)s %(name)s %(message)s", json_schema_extra={"env": "LOG_FORMAT"})
    date_format: str = Field(default="%Y-%m-%d %H:%M:%S", json_schema_extra={"env": "LOG_DATE_FORMAT"})
    file_path: Optional[str] = Field(default=None, json_schema_extra={"env": "LOG_FILE_PATH"})
    max_size: int = Field(default=10485760, json_schema_extra={"env": "LOG_MAX_SIZE"})  # 10MB
    backups: int = Field(default=5, json_schema_extra={"env": "LOG_BACKUPS"})
    log_to_console: bool = Field(default=True, json_schema_extra={"env": "LOG_TO_CONSOLE"})
    use_async: bool = Field(default=True, json_schema_extra={"env": "LOG_USE_ASYNC"})
    use_json: bool = Field(default=False, json_schema_extra={"env": "LOG_USE_JSON"})
    ignore_modules: list[str] = Field(default_factory=lambda: ['pdfminer', 'psparser'], json_schema_extra={"env": "LOG_IGNORE_MODULES"})
