"""

Python just for fun

"""

from datetime import datetime as dt, timedelta

import vk_api
import os

VK_LOGIN = os.environ.get('VK_LOGIN')
VK_PASS = os.environ.get('VK_PASS')
GROUP_ID = 189841908
GROUP_NAME_ORIG = 'Year Progress'


def calculate_year_progress(day: dt = None) -> int:
    day = day or dt.today()

    today_day_number = get_day_number(day)
    days_count_in_year = return_days_count_in_year(day)

    percent = int(today_day_number / days_count_in_year * 100)

    return percent


def get_day_number(day: dt = None) -> int:
    day = day or dt.today()

    new_year_day = dt(day.year, month=1, day=1)
    today_day_number = (day - new_year_day).days + 1

    return today_day_number


def return_days_count_in_year(day: dt = None) -> int:
    day = day or dt.today()

    if is_leap_year(day.year):
        days_count_in_year = 366
    else:
        days_count_in_year = 365

    return days_count_in_year


def prepare_message_percent(percent: int) -> str:
    one = '⬛'
    zero = '⬜'

    bar_length = 10
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


def post_percent() -> None:
    assert VK_LOGIN
    assert VK_PASS

    vk_session = vk_api.VkApi(VK_LOGIN, VK_PASS)
    vk_session.auth()

    vk = vk_session.get_api()

    year_percent = calculate_year_progress()
    message = prepare_message_percent(year_percent)

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


def prepare_message_number(day: int) -> str:
    template = f'Сегодня {day}-й день года.'

    return template


def post_day_count() -> None:
    assert VK_LOGIN
    assert VK_PASS

    vk_session = vk_api.VkApi(VK_LOGIN, VK_PASS)
    vk_session.auth()

    vk = vk_session.get_api()

    day_number = get_day_number()
    message = prepare_message_number(day_number)

    # TODO add retry
    post_response = vk.wall.post(owner_id=f'-{GROUP_ID}', message=message)
    print(post_response)


def is_right_day_to_post_percent(day: dt = None) -> bool:
    """
    Return True if percent of previous day is not equal to percent of day
    :param day:
    :return: True or False
    """

    day = day or dt.today()
    day_before = day - timedelta(days=1)

    orig_day_percent = calculate_year_progress(day)
    day_before_percent = calculate_year_progress(day_before)

    return orig_day_percent != day_before_percent
