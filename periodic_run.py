"""

Periodic runner

"""

from apscheduler.schedulers.blocking import BlockingScheduler
from core import post_percent, is_right_day_to_post_percent, post_day_count, create_yp_logo, load_new_group_cover

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', hour=7)  # 7:00 UTC, 10:00 Moscow
def timed_job():
    if is_right_day_to_post_percent():
        post_percent()
        logo_file_name = create_yp_logo()
        load_new_group_cover(logo_file_name)
    else:
        post_day_count()


scheduler.start()
