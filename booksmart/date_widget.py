from django import forms
from django.forms import DateInput

class MyFlatPickrUni(DateInput):
    template_name = "my_flatpickr_uni"


class DateForm(forms.Form):
    date = forms.DateField(
        input_formats=['%m/%d/%Y'], 
        widget=MyFlatPickrUni()
    )  