from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import management
import codecs

from data_capture.forms import LoadDataForm
from contracts.lib.contractdatareader import ContractDataReader
from contracts.models import Contract


class LoadDataView(FormView):
    template_name = "load.html"
    form_class = LoadDataForm
    success_url = "/data_capture/"

    def clear_contracts(self):
        management.call_command('flush', verbosity=0, interactive=False)

    def load_contracts(self, uploaded_file):
        contracts = list(ContractDataReader().parse(
            codecs.iterdecode(uploaded_file, 'utf-8')))

        Contract.objects.all().delete()

        Contract.objects.bulk_create(contracts)

        management.call_command(
            'update_search_field',
            Contract._meta.app_label, Contract._meta.model_name
        )
        return contracts

    def form_valid(self, form):
        if 'load' in form.data:
            if 'file' not in self.request.FILES:
                messages.add_message(
                    self.request, messages.ERROR, 'File must be selected')
            else:
                uploaded_file = self.request.FILES['file']

                try:
                    contracts = self.load_contracts(uploaded_file)
                    messages.add_message(
                        self.request, messages.SUCCESS,
                        'Loaded %d contract records' % len(contracts)
                    )
                except:
                    messages.add_message(
                        self.request, messages.ERROR,
                        'Unable to read contracts from uploaded file'
                    )
                    print("here")

        elif 'clear' in form.data:
            self.clear_contracts()
            messages.add_message(
                self.request, messages.SUCCESS, 'Data cleared'
            )

        return super(LoadDataView, self).form_valid(form)
