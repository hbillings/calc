from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import LoadDataForm


class LoadDataView(FormView):
    template_name = "load.html"
    form_class = LoadDataForm
    success_url = "/data_capture/"

    def form_valid(self, form):
        if 'load' in form.data:
            form.load_data()
            messages.add_message(
                self.request, messages.SUCCESS, 'Data loaded'
            )
        elif 'clear' in form.data:
            form.clear_data()
            messages.add_message(
                self.request, messages.SUCCESS, 'Data cleared'
            )
        return super(LoadDataView, self).form_valid(form)
