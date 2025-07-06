from datetime import datetime
import pytz

# 获取上海时区对象
shanghai_tz = pytz.timezone('Asia/Shanghai')
# 获取当前时间并设置时区为上海时区
# now_shanghai = datetime.now(shanghai_tz)