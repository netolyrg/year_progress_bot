"""

Periodic runner

"""

from apscheduler.schedulers.blocking import BlockingScheduler
from core import post_message

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    post_message()


sched.start()
