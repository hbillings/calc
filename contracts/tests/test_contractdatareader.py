import os
from collections import OrderedDict
from django.test import TestCase

from contracts.lib.contractdatareader import ContractDataReader
from contracts.constants import FEDERAL_MIN_CONTRACT_RATE


class TestContractDataReader(TestCase):

    def test_make_contract_ok(self):
        full_row = self.make_row()
        ContractDataReader.make_contract(full_row)

        row_without_experience = self.make_row(experience='')
        ContractDataReader.make_contract(row_without_experience)

        row_without_dates = self.make_row(begin_date='', end_date='')
        ContractDataReader.make_contract(row_without_dates)

    def test_make_contract_fails(self):
        row_without_price = self.make_row(year_1='')
        self.assertRaises(
            ValueError,
            ContractDataReader.make_contract,
            row_without_price
        )

    def test_no_display_price_if_too_low(self):
        price = FEDERAL_MIN_CONTRACT_RATE - 1.0
        contract = ContractDataReader.make_contract(
            self.make_row(year_1=str(price)))
        self.assertEquals(contract.hourly_rate_year1, price)
        self.assertIsNone(contract.current_price)

    def test_parse_ok(self):
        file_path = os.path.join(
            os.path.dirname(__file__), 'data/hourly_prices_sample.csv')

        with open(file_path, 'rU') as fileobj:
            contracts = list(ContractDataReader().parse(fileobj))
            self.assertEquals(len(contracts), 2)

    def test_load_file_ok(self):
        file_path = os.path.join(
            os.path.dirname(__file__), 'data/hourly_prices_sample.csv')

        contracts = ContractDataReader().load_file(file_path)
        self.assertEquals(len(contracts), 2)

    def test_parse_does_not_fail(self):
        file_path = os.path.join(
            os.path.dirname(__file__), 'data/hourly_prices_bad.csv')

        with open(file_path, 'rU') as fileobj:
            contracts = list(ContractDataReader().parse(fileobj))
            self.assertEquals(len(contracts), 1)

    def test_load_file_does_not_fail(self):
        file_path = os.path.join(
            os.path.dirname(__file__), 'data/hourly_prices_bad.csv')

        contracts = ContractDataReader().load_file(file_path)
        self.assertEquals(len(contracts), 1)

    def test_parse_strict_mode_fails(self):
        file_path = os.path.join(
            os.path.dirname(__file__), 'data/hourly_prices_bad.csv')

        with open(file_path, 'rU') as fileobj:
            contract_iter = ContractDataReader().parse(fileobj, strict=True)

            self.assertRaises(
                ValueError,
                list,
                contract_iter
            )

    def test_load_file_strict_mode_fails(self):
        file_path = os.path.join(
            os.path.dirname(__file__), 'data/hourly_prices_bad.csv')

        self.assertRaises(
            ValueError,
            ContractDataReader().load_file,
            file_path,
            strict=True
        )

    def make_row(self, **kwargs):
        default = OrderedDict([
            ('labor_category', 'Tester'),
            ('year_1', '38'),
            ('year_2', '39'),
            ('year_3', '40'),
            ('year_4', '41'),
            ('year_5', '42'),
            ('education', 'Bachelors'),
            ('min_years_experience', '1'),
            ('business_size', 'O'),
            ('location', 'Both'),
            ('company_name', 'Test Company'),
            ('contract_number', 'GS-12A-345BC'),
            ('schdule', 'Consolidated'),
            ('sin', 'C874 1, C874 7, C871 1, C871 2, C871 3, C871 4,'),
            ('contract_year', '1'),
            ('begin_date', '1/9/2004'),
            ('end_date', '1/8/2019'),
        ])

        return [kwargs.get(k, v) for k, v in default.items()]
