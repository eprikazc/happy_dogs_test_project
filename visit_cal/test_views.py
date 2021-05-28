from datetime import date

from model_bakery import baker
import pytest

from visit_cal.models import Visit


def test_CalendarView_ReturnsOK(db, client, visits):
    response = client.get('/?start_date=2021-05-04&end_date=2021-05-07')
    assert response.status_code == 200
    assert response.context['days'] == [
        {'date': date(2021, 5, 3), 'show': False, 'dogs_count': 0},  # Monday
        {'date': date(2021, 5, 4), 'show': True, 'dogs_count': 1},
        {'date': date(2021, 5, 5), 'show': True, 'dogs_count': 2},
        {'date': date(2021, 5, 6), 'show': True, 'dogs_count': 1},
        {'date': date(2021, 5, 7), 'show': True, 'dogs_count': 0},
        {'date': date(2021, 5, 8), 'show': False, 'dogs_count': 0},
        {'date': date(2021, 5, 9), 'show': False, 'dogs_count': 0},
    ]


def test_DayVisitsView_ReturnsOK(db, client, visits):
    visit1, visit2 = visits
    response = client.get('/2021/05/5/')
    assert response.status_code == 200
    qs = response.context['visits']
    assert list(qs.values_list('id', flat=True)) == [visit1.pk, visit2.pk]


@pytest.fixture
def visits(db):
    visit1 = baker.make(Visit, start_date=date(2021, 5, 4), end_date=date(2021, 5, 5))
    visit2 = baker.make(Visit, start_date=date(2021, 5, 5), end_date=date(2021, 5, 6))
    return (visit1, visit2)
