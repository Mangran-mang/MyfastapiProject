from datetime import datetime
from zoneinfo import ZoneInfo
from langchain.tools import tool
import time



class Tools:
    @tool
    @staticmethod
    def get_current_time():
        """获取当前时间"""
        # 北京时间对应的时区ID是 "Asia/Shanghai"（标准时区）
        beijing_tz = ZoneInfo("Asia/Shanghai")
        # 获取当前东八区时间
        beijing_time = datetime.now(beijing_tz)
        # 格式化为字符串返回
        return beijing_time.strftime("%Y-%m-%d %H:%M:%S")