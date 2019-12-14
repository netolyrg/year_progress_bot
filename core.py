"""

Python just for fun

"""

from datetime import datetime as dt

import vk_api
import os

VK_LOGIN = os.environ.get('VK_LOGIN')
VK_PASS = os.environ.get('VK_PASS')
GROUP_ID = '-189841908'


def calculate_year_progress():
    today = dt.today()

    if is_leap_year(today.year):
        days_count_in_year = 366
    else:
        days_count_in_year = 365

    new_year_day = dt(today.year, month=1, day=1)
    today_day_number = (today - new_year_day).days + 1

    percent = int(today_day_number / days_count_in_year * 100)

    return str(percent)


def prepare_message(percent):
    return 'Прогресс года: {}%!'.format(percent)


def is_leap_year(year):
    if year % 4 == 0:
        return True
    else:
        return False


def post_message():
    assert VK_LOGIN
    assert VK_PASS

    vk_session = vk_api.VkApi(VK_LOGIN, VK_PASS)
    vk_session.auth()

    vk = vk_session.get_api()

    message = prepare_message(calculate_year_progress())

    print(vk.wall.post(owner_id=GROUP_ID, message=message))


if __name__ == '__main__':
    post_message()
