"""

Test for core

"""

from freezegun import freeze_time

from core import calculate_year_progress, is_leap_year, prepare_message, get_new_name, is_right_day


@freeze_time('2019-07-02')
def test_calc_datetime_50_percent():
    percent = calculate_year_progress()

    assert percent == 50


@freeze_time('2019-12-31')
def test_calc_datetime_100_percent():
    percent = calculate_year_progress()

    assert percent == 100


@freeze_time('2019-01-01')
def test_calc_datetime_0_percent():
    percent = calculate_year_progress()

    assert percent == 0


def test_leap_year():
    assert is_leap_year(2020) is True


def test_not_leap_year():
    assert is_leap_year(2019) is False


def test_message_creation_50_percent():
    message = prepare_message(50)

    assert message == '⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜ 50%!'


def test_message_creation_100_percent():
    message = prepare_message(100)

    assert message == '⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛ 100%!'


def test_message_creation_0_percent():
    message = prepare_message(0)

    assert message == '⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%!'


def test_new_name_creation():
    name = get_new_name('test', 50)

    expected = 'test | 50%'

    assert name == expected


@freeze_time('2019-12-17')
def test_right_day():
    assert is_right_day() is True


@freeze_time('2019-12-16')
def test_not_right_day():
    assert is_right_day() is False
