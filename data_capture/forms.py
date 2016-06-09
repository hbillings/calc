from django import forms
from django.core import management


class LoadDataForm(forms.Form):

    def load_data(self):
        management.call_command('load_data', verbosity=0)
        management.call_command('load_s70', verbosity=0)

    def clear_data(self):
        management.call_command('flush', verbosity=0, interactive=False)
