"""

Python just for fun

"""

from datetime import datetime as dt

import vk_api
import os

VK_LOGIN = os.environ.get('VK_LOGIN')
VK_PASS = os.environ.get('VK_PASS')
GROUP_ID = 189841908
GROUP_NAME_ORIG = 'Year Progress'


def calculate_year_progress() -> int:
    today = dt.today()

    if is_leap_year(today.year):
        days_count_in_year = 366
    else:
        days_count_in_year = 365

    new_year_day = dt(today.year, month=1, day=1)
    today_day_number = (today - new_year_day).days + 1

    percent = int(today_day_number / days_count_in_year * 100)

    return percent


def prepare_message(percent: int) -> str:
    one = '⬛'
    zero = '⬜'

    bar_length = 18
    bar_percent = int(percent / 100 * bar_length)

    return '{}{} {}%!'.format(one * bar_percent, zero * (bar_length - bar_percent), percent)


def is_leap_year(year: int) -> bool:
    if year % 4 == 0:
        return True
    else:
        return False


def get_new_name(old_name: str, year_percent: int) -> str:
    return '{} | {}%'.format(old_name, year_percent)


def get_status(percent: int) -> str:
    if percent == 0:
        text = 'Год только начался!'
    elif percent == 33:
        text = 'Уже треть прошла...'
    elif percent == 50:
        text = 'Через полгода Новый год!'
    elif percent == 67:
        text = '2/3 года позади'
    else:
        text = '{}% года за плечами'.format(percent)

    return text


def post_message():
    assert VK_LOGIN
    assert VK_PASS

    vk_session = vk_api.VkApi(VK_LOGIN, VK_PASS)
    vk_session.auth()

    vk = vk_session.get_api()

    year_percent = calculate_year_progress()
    message = prepare_message(year_percent)

    status = get_status(year_percent)

    new_name = get_new_name(GROUP_NAME_ORIG, year_percent)

    # TODO add retry
    post_response = vk.wall.post(owner_id=f'-{GROUP_ID}', message=message)
    print(post_response)

    # TODO add retry
    status_response = vk.status.set(group_id=GROUP_ID, text=status)
    print(status_response)

    # TODO add retry
    rename_response = vk.groups.edit(group_id=GROUP_ID, title=new_name)
    print(rename_response)


if __name__ == '__main__':
    post_message()
