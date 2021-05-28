from datetime import date, timedelta
import random

from faker import Faker

from visit_cal.forms import VisitForm
from visit_cal.models import Dog


fake = Faker()


def gen_data(
        dogs_range=range(5, 10), visits_range=range(5, 10),
        start_date=date(2021, 1, 1), end_date=date(2021, 12, 31)):
    Dog.objects.all().delete()
    dogs_count = random.choice(dogs_range)
    days = (end_date - start_date).days
    for _ in range(dogs_count):
        d = Dog.objects.create(
           first_name=fake.first_name(),
           last_name=random.choice(["", fake.last_name()]))
        visit_count = random.choice(visits_range)
        for _ in range(visit_count):
            board_date = start_date + timedelta(days=random.choice(range(days)))
            departure_date = board_date + timedelta(days=random.choice(range(2, 7)))
            f = VisitForm({
                'start_date': board_date,
                'end_date': departure_date,
                'dog': d,
            })
            if f.is_valid():
                f.save()
