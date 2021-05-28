from django.db import models


class Dog(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = [('first_name', 'last_name')]

    def __str__(self):
        return " ".join([self.first_name, self.last_name]).strip()


class VisitQuerySet(models.QuerySet):
    def between(self, start, end):
        return self.filter(
            models.Q(start_date__range=(start, end))
            | models.Q(end_date__range=(start, end))
            | models.Q(start_date__lte=start, end_date__gte=end)
        )


class Visit(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)

    objects = VisitQuerySet.as_manager()

    def dates_repr(self):
        return "%s-%s" % (self.start_date.isoformat(), self.end_date.isoformat())
