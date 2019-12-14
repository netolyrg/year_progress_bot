"""

Periodic runner

"""

from apscheduler.schedulers.blocking import BlockingScheduler
from core import post_message

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', hour=8)
def timed_job():
    post_message()


scheduler.start()
