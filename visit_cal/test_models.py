from datetime import date, timedelta

from model_bakery import baker

from visit_cal.models import Visit


START_DATE = date(2021, 5, 1)
END_DATE = date(2021, 5, 10)
DATE_BEFORE = date(2021, 4, 25)
DATE_WITHIN = date(2021, 5, 5)
DATE_AFTER = date(2021, 5, 25)


def test_VisitBefore_IsNotIncludedInBetween(db):
    baker.make("Visit", start_date=DATE_BEFORE, end_date=DATE_BEFORE+timedelta(days=2))
    assert Visit.objects.between(START_DATE, END_DATE).count() == 0


def test_VisitAfter_IsNotIncludedInBetween(db):
    baker.make("Visit", start_date=DATE_AFTER, end_date=DATE_AFTER+timedelta(days=2))
    assert Visit.objects.between(START_DATE, END_DATE).count() == 0


def test_VisitWithin_IsIncludedInBetween(db):
    baker.make("Visit", start_date=DATE_WITHIN, end_date=DATE_WITHIN+timedelta(days=2))
    assert Visit.objects.between(START_DATE, END_DATE).count() == 1


def test_VisitThatFinishesWithin_IsIncludedInBetween(db):
    baker.make("Visit", start_date=DATE_BEFORE, end_date=DATE_WITHIN)
    assert Visit.objects.between(START_DATE, END_DATE).count() == 1


def test_VisitThatStartsWithin_IsIncludedInBetween(db):
    baker.make("Visit", start_date=DATE_WITHIN, end_date=DATE_AFTER)
    assert Visit.objects.between(START_DATE, END_DATE).count() == 1


def test_VisitOnLeftBounday_IsIncludedInBetween(db):
    baker.make("Visit", start_date=DATE_BEFORE, end_date=START_DATE)
    assert Visit.objects.between(START_DATE, END_DATE).count() == 1


def test_VisitOnRightBounday_IsIncludedInBetween(db):
    baker.make("Visit", start_date=END_DATE, end_date=DATE_AFTER)
    assert Visit.objects.between(START_DATE, END_DATE).count() == 1
