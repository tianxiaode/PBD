from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class CalendarType(str, Enum):
    GREGORIAN = "Gregorian"
    LUNAR = "Lunar"
    JAPANESE = "Japanese"
    OTHER = "Other"

class TextDirection(str, Enum):
    LEFT_TO_RIGHT = "left-to-right"
    RIGHT_TO_LEFT = "right-to-left"

class MeasurementSystem(str, Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"

class FirstDayOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"

class CultureInfo(BaseModel):
    # 标识信息
    name: str = Field(..., min_length=1, max_length=100)  # 如 "English", "中文"
    display_name: str = Field(..., min_length=1, max_length=100)  # 如 "English (United States)", "中文 (中国)"
    language_code: str = Field(..., min_length=2, max_length=5)  # 如 "en", "zh-CN"
    country_code: str = Field(..., min_length=2, max_length=5)   # 如 "US", "CN"
    
    # 日期时间格式
    date_time_format: str = "YYYY-MM-DD HH:mm:ss"
    date_format: str = "YYYY-MM-DD"
    time_format: str = "HH:mm:ss"
    short_date_format: str = "YY-MM-DD"
    short_time_format: str = "HH:mm"
    
    # 数字和货币格式
    number_decimal_separator: str = "."
    number_group_separator: str = ","
    currency_symbol: str = "$"
    currency_format: str = "{0}{1}"  # 0=金额, 1=符号
    
    # 其他设置
    calendar_type: CalendarType = CalendarType.GREGORIAN
    first_day_of_week: str = FirstDayOfWeek.MONDAY
    text_direction: TextDirection = TextDirection.LEFT_TO_RIGHT
    measurement_system: MeasurementSystem = MeasurementSystem.METRIC
    
    # 可选的高级设置
    time_zone: Optional[str] = "UTC"
    week_days_full: List[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    week_days_abbr: List[str] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    holidays: List[str] = []
    months_full: List[str] = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    months_abbr: List[str] = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
