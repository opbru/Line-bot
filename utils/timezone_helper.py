# utils/timezone_helper.py
import pytz
from datetime import datetime
from datetime import timedelta

# 定義台北時區
TAIPEI_TZ = pytz.timezone('Asia/Taipei')

def get_taipei_time():
    """獲取當前台北時間"""
    return datetime.now(TAIPEI_TZ)

def to_taipei_time(dt):
    """將時間轉換為台北時間"""
    if dt is None:
        return None

    # 如果已經有時區資訊
    if dt.tzinfo is not None:
        return dt.astimezone(TAIPEI_TZ)

    # 如果沒有時區資訊，假設是 UTC
    utc_dt = pytz.UTC.localize(dt)
    return utc_dt.astimezone(TAIPEI_TZ)

def format_taipei_time(dt, format_string='%m/%d %H:%M'):
    """格式化為台北時間字串"""
    if dt is None:
        return ''

    taipei_dt = to_taipei_time(dt)
    return taipei_dt.strftime(format_string)

def get_start_of_week():
    """取得本週開始時間（週一 00:00）"""
    today = get_taipei_time()
    start_of_week = today - timedelta(days=today.weekday())
    return start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
