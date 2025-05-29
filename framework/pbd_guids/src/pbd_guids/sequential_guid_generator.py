import os
import uuid
import time
from threading import Lock
from .interfaces import IGuidGenerator

class SequentialGuidGenerator(IGuidGenerator):
    """可靠的16字节GUID生成器，避免重复"""
    _lock = Lock()
    _last_timestamp = 0
    _sequence = 0

    def create(self) -> uuid.UUID:
        """生成严格16字节的UUID"""
        with self._lock:
            # 使用更高精度的时间（微秒级）
            current_time = time.time_ns() // 1000
            if current_time < self._last_timestamp:
                current_time = self._last_timestamp + 1

            if current_time == self._last_timestamp:
                self._sequence += 1
                if self._sequence > 0xFFFF:
                    self._sequence = 0
                    current_time += 1
            else:
                self._sequence = 0

            self._last_timestamp = current_time

            # 准备各部分字节
            timestamp_bytes = current_time.to_bytes(8, 'big')[-6:]  # 取低6字节
            sequence_bytes = self._sequence.to_bytes(2, 'big')

            guid_bytes = bytearray(16)

                # 动态生成随机部分，避免重复
            random_bytes = os.urandom(8)
            guid_bytes[0:6] = timestamp_bytes
            guid_bytes[6:8] = sequence_bytes
            guid_bytes[8:16] = random_bytes


            return uuid.UUID(bytes=bytes(guid_bytes))



# class UniversalUUID(TypeDecorator):
#     impl = CHAR(36)
#     cache_ok = True

#     def process_bind_param(self, value, dialect):
#         if value is None:
#             return None
#         if isinstance(value, uuid.UUID):
#             return str(value)
#         return str(uuid.UUID(value))  # 保证都是合法 UUID 字符串

#     def process_result_value(self, value, dialect):
#         if value is None:
#             return None
#         return uuid.UUID(value)
