from datetime import date, timedelta
import random

from faker import Faker

from visit_cal.forms import VisitForm
from visit_cal.models import Dog


fake = Faker()

US_HOLIDAYS = [
    date(2021, 1, 1),
    date(2021, 1, 18),
    date(2021, 2, 15),
    date(2021, 5, 31),
    date(2021, 7, 4),
    date(2021, 9, 6),
    date(2021, 10, 11),
    date(2021, 11, 11),
    date(2021, 11, 25),
    date(2021, 12, 25),
    date(2021, 12, 31),
]


def gen_data(
        dogs_range=range(20, 30), visits_range=range(10, 15),
        start_date=date(2021, 1, 1), end_date=date(2021, 12, 31)):
    Dog.objects.all().delete()
    dogs_count = random.choice(dogs_range)
    available_dates = []
    weights = []
    current_date = start_date
    while current_date <= end_date:
        available_dates.append(current_date)
        weights.append(_get_weight(current_date))
        current_date += timedelta(days=1)
    for _ in range(dogs_count):
        d = Dog.objects.create(
           first_name=fake.first_name(),
           last_name=random.choice(["", fake.last_name()]))
        visit_count = random.choice(visits_range)
        board_dates = random.choices(available_dates, weights, k=visit_count)
        for board_date in board_dates:
            departure_date = board_date + timedelta(days=random.choice(range(1, 6)))
            f = VisitForm({
                'start_date': board_date,
                'end_date': departure_date,
                'dog': d,
            })
            if f.is_valid():
                f.save()


def _get_weight(date):
    assert date.year == 2021
    for holiday in US_HOLIDAYS:
        two_days_before = holiday - timedelta(days=2)
        two_days_after = holiday + timedelta(days=2)
        if date >= two_days_before and date <= two_days_after:
            return 15
    if date.weekday() in (5, 6):
        return 5
    return 1
