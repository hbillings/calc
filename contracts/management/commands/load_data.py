from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from contracts.models import Contract
from contracts.constants import FEDERAL_MIN_CONTRACT_RATE
import os
import logging
from datetime import datetime, date

from contracts.lib.contractdatareader import ContractDataReader


class Command(BaseCommand):

    def handle(self, *args, **options):
        log = logging.getLogger(__name__)

        log.info("Begin load_data task")

        log.info("Deleting existing contract records")
        Contract.objects.all().delete()

        file_path = os.path.join(
            settings.BASE_DIR, 'contracts/docs/hourly_prices.csv')
        try:
            contracts = ContractDataReader().load_file(file_path)
        except Exception as e:
            log.exception(e)
            exit(1)

        log.info("Inserting %d records" % len(contracts))
        Contract.objects.bulk_create(contracts)

        log.info("Updating search index")
        call_command(
            'update_search_field',
            Contract._meta.app_label, Contract._meta.model_name
        )

        log.info("End load_data task")
