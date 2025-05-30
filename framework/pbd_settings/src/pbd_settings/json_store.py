import os
import json
import threading
from pbd_core import find_project_root
from .interfaces import IJsonSettingStore
from .schema import SettingDefinition

class JsonSettingStore(IJsonSettingStore):
    def initailize(self, env=None):
        self._env = env or os.getenv('APP_ENV', 'development')
        self._lock = threading.Lock()
        self._cache = None
        self._loaded = False

    async def get(self, provider_name, setting: SettingDefinition):
        settings = await self._get_settings()
        return settings.get(setting.name)

    async def get_all(self, provider_name, settings):
        all_settings = await self._get_settings()
        return {setting.name: all_settings.get(setting.name) for setting in settings}

    async def _get_settings(self):
        if not self._loaded:
            await self.load()
        return self._cache

    async def load(self):

        config_file = self.get_config_file_path()
        with self._lock:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._cache = self._flatten_dict(data)
                self._loaded = True

    def get_config_file_path(self):
        project_root = find_project_root()
        config_file = project_root / 'config' / f'{self._env}.json'

        if not config_file.exists():
            raise FileNotFoundError(f'配置文件未找到: {config_file}')
        return config_file


    def _flatten_dict(self, d, parent_key='', sep='.'):
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, new_key, sep=sep))
            else:
                items[new_key] = v
        return items

