from django import forms

from visit_cal.models import Visit


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ("dog", "start_date", "end_date")

    def clean(self):
        dog = self.cleaned_data.get("dog")
        start = self.cleaned_data.get("start_date")
        end = self.cleaned_data.get("end_date")
        if not (dog and start and end):
            # Required fields are missing, no need to perform extra validation
            return
        if start >= end:
            raise forms.ValidationError("Start date must be earlier than end date")
        overlapping_visits = Visit.objects.filter(dog=dog).between(start, end).order_by("start_date")
        if overlapping_visits:
            raise forms.ValidationError(
                "Overlapping visits exist: " +
                ", ".join([v.dates_repr() for v in overlapping_visits]))


class DatesForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

    def clean(self):
        start = self.cleaned_data.get("start_date")
        end = self.cleaned_data.get("end_date")
        if start and end and start >= end:
            raise forms.ValidationError("Start date must be earlier than end date")
