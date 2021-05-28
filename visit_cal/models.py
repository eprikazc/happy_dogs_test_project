from django.db import models


class Dog(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = [('first_name', 'last_name')]

    def __str__(self):
        return " ".join([self.first_name, self.last_name]).strip()


class Visit(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)

    def dates_repr(self):
        return "%s-%s" % (self.start_date.isoformat(), self.end_date.isoformat())
