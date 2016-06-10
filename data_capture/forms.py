from django import forms


class LoadDataForm(forms.Form):
    file = forms.FileField()
