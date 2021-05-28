from datetime import date

from model_bakery import baker
import pytest

from visit_cal.forms import VisitForm


def test_WhenDatesOK_VisitFormValid(dog):
    form = VisitForm({"dog": dog, "start_date": "2021-05-01", "end_date": "2021-05-04"})
    assert form.is_valid() is True


def test_WhenDateSwapped_VisitFormInvalid(dog):
    form = VisitForm({"dog": dog, "start_date": "2021-05-05", "end_date": "2021-05-01"})
    assert form.is_valid() is False
    assert form.errors == {'__all__': ['Start date must be earlier than end date']}


def test_WhenOverlap_VisitFormInvalid(dog):
    baker.make("Visit", dog=dog, start_date=date(2021, 5, 1), end_date=date(2021, 6, 1))
    form = VisitForm({"dog": dog, "start_date": "2021-05-01", "end_date": "2021-05-05"})
    assert form.is_valid() is False
    assert form.errors == {'__all__': ['Overlapping visits exist: 2021-05-01:2021-06-01']}


def test_WhenOverlapWithAnotherDog_VisitFormvalid(dog):
    another_dog = baker.make("Dog")
    baker.make("Visit", dog=another_dog, start_date=date(2021, 5, 1), end_date=date(2021, 6, 1))
    form = VisitForm({"dog": dog, "start_date": "2021-05-01", "end_date": "2021-05-05"})
    assert form.is_valid() is True


@pytest.fixture
def dog(db):
    return baker.make("Dog")
