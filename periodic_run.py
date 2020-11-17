"""

Periodic runner

"""

import os

from apscheduler.schedulers.blocking import BlockingScheduler

from core import (
    post_percent,
    is_right_day_to_post_percent,
    post_day_count,
    create_yp_logo,
    load_new_group_cover,
    post_new_year_countdown
)

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', hour=7)  # 7:00 UTC, 10:00 Moscow
def timed_job():
    if is_right_day_to_post_percent():
        post_percent()
        logo_file_name = create_yp_logo()
        load_new_group_cover(logo_file_name)
    else:
        post_day_count()


@scheduler.scheduled_job('cron', hour=11)  # 11:00 UTC, 14:00 Moscow
def timed_job():
    new_year_feature_enabled = os.environ.get('NEW_YEAR_FEATURE_ENABLED', False)
    if new_year_feature_enabled:
        post_new_year_countdown()


scheduler.start()
