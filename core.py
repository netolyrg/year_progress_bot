"""

Python just for fun

"""

import os
from datetime import datetime as dt, timedelta
from random import choice

import vk_api
from PIL import Image, ImageDraw, ImageFont
from phrases import NY_PHRASES

VK_LOGIN = os.environ.get('VK_LOGIN')
VK_PASS = os.environ.get('VK_PASS')
GROUP_ID = 189841908
GROUP_NAME_ORIG = 'Year Progress'

NEW_YEAR_FEATURE_ENABLED = bool(os.environ.get('NEW_YEAR_FEATURE_ENABLED', False))


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


def post_day_count(image_file_name=None) -> None:
    assert VK_LOGIN
    assert VK_PASS

    vk_session = vk_api.VkApi(VK_LOGIN, VK_PASS)
    vk_session.auth()

    vk = vk_session.get_api()

    day_number = get_day_number()
    message = prepare_message_number(day_number)

    if image_file_name:
        upload = vk_api.VkUpload(vk_session)
        photo = upload.photo_wall(
            image_file_name,
            group_id=GROUP_ID,
        )[0]

        owner_id, media_id = photo.get('owner_id'), photo.get('id')
        photo_attachment = f'photo{owner_id}_{media_id}'

        data_to_post = dict(owner_id=f'-{GROUP_ID}', message=message, attachments=photo_attachment)
    else:
        data_to_post = dict(owner_id=f'-{GROUP_ID}', message=message)

    # TODO add retry
    post_response = vk.wall.post(**data_to_post)
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


# todo need tests
def create_yp_logo() -> str:
    file_name = 'yp_cover.png'
    title_size = 42
    percent_size = 250
    image_size = (700, 700)

    percent = calculate_year_progress()
    text_percent = f'{percent}%'
    text_title = 'Year Progress'

    img = Image.new(mode='RGB', color=(255, 255, 255), size=image_size)
    draw = ImageDraw.Draw(img)
    font_percent = ImageFont.truetype('fonts/Roboto-Medium.ttf', size=percent_size)
    font_title = ImageFont.truetype('fonts/Roboto-Regular.ttf', size=title_size)

    width, height = image_size

    # percent
    percent_width, percent_height = font_percent.getsize(text_percent)[0], 293
    x, y = (width - percent_width) // 2, (height - percent_height - 25) // 2
    draw.text((x, y), text_percent, fill=(0, 0, 0), font=font_percent)

    # title
    title_width, title_height = 254, 49
    x, y = (width - title_width - 2) // 2, (height - title_height + 279) // 2
    draw.text((x, y), text_title, fill=(177, 177, 177), font=font_title)

    img.save(file_name)

    return file_name


# todo need tests
def create_yp_number_image() -> str:
    file_name = 'yp_number.png'
    title_size = 42
    percent_size = 56
    image_size = (700, 700)

    day_number = get_day_number()
    text_number = prepare_message_number(day_number).replace('.', '')
    text_title = 'Year Progress'

    img = Image.new(mode='RGB', color=(255, 255, 255), size=image_size)
    draw = ImageDraw.Draw(img)
    font_percent = ImageFont.truetype('fonts/Roboto-Medium.ttf', size=percent_size)
    font_title = ImageFont.truetype('fonts/Roboto-Regular.ttf', size=title_size)

    width, height = image_size

    # percent
    percent_width, percent_height = font_percent.getsize(text_number)[0], font_percent.getsize(text_number)[1]
    x, y = (width - percent_width) // 2, (height - percent_height - 25) // 2
    draw.text((x, y), text_number, fill=(0, 0, 0), font=font_percent)

    # title
    title_width, title_height = 254, 49
    x, y = (width - title_width - 2) // 2, (height - title_height + 120) // 2
    draw.text((x, y), text_title, fill=(177, 177, 177), font=font_title)

    img.save(file_name)

    return file_name


def load_new_group_cover(cover_file: str) -> None:
    assert VK_LOGIN
    assert VK_PASS

    vk_session = vk_api.VkApi(VK_LOGIN, VK_PASS)
    vk_session.auth(token_only=True)

    upload = vk_api.VkUpload(vk_session)
    photo = upload.photo_profile(
        cover_file,
        owner_id=-GROUP_ID,
    )

    photo_post_id = photo.get('post_id')

    vk = vk_session.get_api()
    vk.wall.delete(
        owner_id=-GROUP_ID,
        post_id=photo_post_id
    )


def get_days_before_new_year() -> int:
    year = dt.now().year
    # 31 of december from 365 days == 1 day before New Year
    # 31 of december from 366 days == 1 day before New Year
    return 366 - get_day_number() + int(is_leap_year(year))


def generate_ny_countdown_text(orig_days: int, phrase: str = 'Всего {orig_days} {word} до Нового года :)') -> str:
    day_map = {
        (1,): 'день',
        (2, 3, 4): 'дня',
        (5, 6, 7, 8, 9, 0): 'дней',
    }

    if orig_days % 100 in (11, 12, 13, 14):
        word = 'дней'
    else:
        for rng, value in day_map.items():
            if orig_days % 10 in rng:
                word = value
                break

    return phrase.format(orig_days=orig_days, word=word)


def post_new_year_countdown():
    assert VK_LOGIN
    assert VK_PASS

    vk_session = vk_api.VkApi(VK_LOGIN, VK_PASS)
    vk_session.auth()

    vk = vk_session.get_api()

    days_before_new_year = get_days_before_new_year()
    phrase = choice(NY_PHRASES)
    post_text = generate_ny_countdown_text(days_before_new_year, phrase=phrase)

    post_response = vk.wall.post(owner_id=f'-{GROUP_ID}', message=post_text)
    print(post_response)

    post_id = post_response.get('post_id')
    if post_id:
        pin_response = vk.wall.pin(owner_id=f'-{GROUP_ID}', post_id=post_id)
        print(pin_response)


if __name__ == '__main__':
    if is_right_day_to_post_percent():
        post_percent()
        logo_file_name = create_yp_logo()
        load_new_group_cover(logo_file_name)
    else:
        image_name = create_yp_number_image()
        post_day_count(image_file_name=image_name)
