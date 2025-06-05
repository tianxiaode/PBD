from typing import Dict


class DictHelper:

    @classmethod
    def flatten(self, source: dict, parent_key='', sep='.') -> dict:
        result = {}
        for k, v in source.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                # 即使v是空字典，也要保留它
                flattened = self.flatten(v, new_key, sep=sep)
                if not flattened:  # 如果子字典是空的
                    result[new_key] = {}
                else:
                    result.update(flattened)
            else:
                result[new_key] = v
        return result