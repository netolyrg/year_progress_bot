"""

Periodic runner

"""

from apscheduler.schedulers.blocking import BlockingScheduler
from core import post_message, is_right_day

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', hour=4)  # 4:00 UTC, 7:00 Moscow
def timed_job():
    if is_right_day():
        post_message()


scheduler.start()
