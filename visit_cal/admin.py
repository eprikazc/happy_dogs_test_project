from django.contrib import admin

from visit_cal.forms import VisitForm
from visit_cal.gen_data import gen_data
from visit_cal.models import Dog, Visit


@admin.action(description='Generate fake data')
def _gen_data(modeladmin, request, queryset):
    gen_data()


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    actions = [_gen_data]
    list_display = ('first_name', 'last_name')


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    form = VisitForm
    list_display = ('dog', 'start_date', 'end_date')
    ordering = ['start_date']
