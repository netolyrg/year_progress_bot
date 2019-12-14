"""

Test for core

"""

from freezegun import freeze_time

from core import calculate_year_progress, is_leap_year, prepare_message


@freeze_time('2019-07-02')
def test_calc_datetime_50_percent():
    percent = calculate_year_progress()

    assert percent == '50'


@freeze_time('2019-12-31')
def test_calc_datetime_100_percent():
    percent = calculate_year_progress()

    assert percent == '100'


@freeze_time('2019-01-01')
def test_calc_datetime_0_percent():
    percent = calculate_year_progress()

    assert percent == '0'


def test_leap_year():
    assert is_leap_year(2020) is True


def test_not_leap_year():
    assert is_leap_year(2019) is False


def test_message_creation():
    message = prepare_message(50)

    assert message == 'Прогресс года: 50%!'
