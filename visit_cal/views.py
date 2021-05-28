from datetime import timedelta
from django.shortcuts import render

from visit_cal.forms import DatesForm
from visit_cal.models import Visit


def calendar(request):
    template_name = 'calendar.html'
    form = DatesForm(request.GET)
    if not form.is_valid():
        return render(request, template_name, {'form': form})
    days = []
    start = form.cleaned_data['start_date']
    end = form.cleaned_data['end_date']
    matching_visits = Visit.objects.between(start, end)
    start_monday = start - timedelta(days=start.weekday())
    end_sunday = end + timedelta(6 - end.weekday())
    current_date = start_monday
    while current_date <= end_sunday:
        should_show = start <= current_date and current_date <= end
        days.append({
            "date": current_date,
            "show": should_show,
            "dogs_count": len([
                v for v in matching_visits
                if v.start_date <= current_date and v.end_date >= current_date
            ]),
        })
        current_date += timedelta(days=1)
    return render(request, template_name, {'form': form, 'days': days})
