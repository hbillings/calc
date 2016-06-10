from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import csv
import os
from datetime import datetime, date

from contracts.constants import FEDERAL_MIN_CONTRACT_RATE
from contracts.models import Contract


class ContractDataReader():
    header_rows = 1

    def load_file(self, filename, strict=False):
        with open(filename, 'rU') as f:
            return list(self.parse(f, strict))

    def parse(self, fileobj, strict=False):
        reader = csv.reader(fileobj)

        for _ in range(self.header_rows):
            next(reader)

        for row in reader:
            try:
                yield self.make_contract(row)
            except ValueError as e:
                if strict:
                    raise

    @classmethod
    def make_contract(cls, line):
        if line[0]:
            # create contract record, unique to vendor, labor cat
            idv_piid = line[11]
            vendor_name = line[10]
            labor_category = line[0].strip().replace('\n', ' ')

            contract = Contract()
            contract.idv_piid = idv_piid
            contract.labor_category = labor_category
            contract.vendor_name = vendor_name

            contract.education_level = contract.get_education_code(line[6])
            contract.schedule = line[12]
            contract.business_size = line[8]
            contract.contract_year = line[14]
            contract.sin = line[13]

            if line[15] != '':
                contract.contract_start = datetime.strptime(
                    line[15], '%m/%d/%Y').date()
            if line[16] != '':
                contract.contract_end = datetime.strptime(
                    line[16], '%m/%d/%Y').date()

            if line[7].strip() != '':
                contract.min_years_experience = line[7]
            else:
                contract.min_years_experience = 0

            if line[1] and line[1] != '':
                contract.hourly_rate_year1 = contract.normalize_rate(
                    line[1])
            else:
                # there's no pricing info
                raise ValueError('missing price')

            for count, rate in enumerate(line[2:6]):
                if rate and rate.strip() != '':
                    setattr(contract, 'hourly_rate_year' +
                            str(count + 2), contract.normalize_rate(rate))

            if line[14] and line[14] != '':
                price_fields = {
                    'current_price': getattr(
                        contract, 'hourly_rate_year' + str(line[14]), 0
                    )
                }
                current_year = int(line[14])
                # we have up to five years of rate data
                if current_year < 5:
                    price_fields['next_year_price'] = getattr(
                        contract,
                        'hourly_rate_year' + str(current_year + 1),
                        0)
                    if current_year < 4:
                        price_fields['second_year_price'] = getattr(
                            contract,
                            'hourly_rate_year' + str(current_year + 2),
                            0)

                # don't create display prices for records where the rate
                # is under the federal minimum contract rate
                for field in price_fields:
                    price = price_fields.get(field)
                    if price and price >= FEDERAL_MIN_CONTRACT_RATE:
                        setattr(contract, field, price)

            contract.contractor_site = line[9]
            return contract


def from_sched70_csv():
    # load_s70.py already has a Schedule70Loader class that could be used
    raise NotImplementedError
