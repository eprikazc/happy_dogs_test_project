from django.contrib import admin

from visit_cal.forms import VisitForm
from visit_cal.models import Dog, Visit


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    pass


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    form = VisitForm
