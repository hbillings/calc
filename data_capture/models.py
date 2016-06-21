from django.db import models

from contracts.models import EDUCATION_CHOICES

DOMESTICITY_CHOICES = (
    ('D', 'Domestic Only'),
    ('O', 'Overseas Only'),
    ('W', 'Worldwide')
)

SITE_CHOICES = (
    ('CON', 'Contractor Site'),
    ('CUS', 'Customer Site'),
    ('BOTH', 'Both')
)


# PriceList is a model for storing the data when a price list XLS is uploaded
# A PriceList has many PriceRows
# None of the fields described in this model are in the example XLS,
# so they would probably need to be gathered through a form.
class PriceList(models.Model):
    idv_piid = models.CharField(
        help_text="Contract Number"
    )

    schedule = models.CharField(
        help_text="Schedule"
    )

    contract_start = models.DateField(null=True, blank=True)
    contract_end = models.DateField(null=True, blank=True)
    contract_year = models.IntegerField(null=True, blank=True)

    is_approved = models.BooleanField(default=False)

    # TODO: Uncomment once User models are added
    # owner = models.ForeignKey(User)
    # approver = models.ForeignKey(User, null=True)
    approval_date = models.DateField(null=True, blank=True)


# This model is based on the contractor (not sched 70) price proposal
# excel sheet that was provided to us as an example.
# It should be trimmed down to only the necessary fields, possibly those
# described by FLIFCALC.
# https://github.com/18F/calc/wiki/Federal-Labor-Interchange-Format-for-CALC
class PriceListRow(models.Model):
    sin = models.CharField(
        help_text="Proposed Special Item Numbers (SINs)"
    )

    labor_category = models.CharField(
        help_text="Labor Category"
    )

    education_level = models.CharField(
        db_index=True, choices=EDUCATION_CHOICES, max_length=5,
        null=True, blank=True, help_text="Minimum Education Level")

    minimum_education_years = models.IntegerField(
        help_text="Minimum Years of Education"
    )

    contractor_site = models.CharField(
        choices=SITE_CHOICES,
        help_text="Customer Site, Contractor Site, or Both"
    )

    # TODO: This might not be necessary if CALC is only supposed to show
    # worldride rates
    domesticity = models.CharField(
        choices=DOMESTICITY_CHOICES,
        help_text="Domestic, Overseas, or Worldwide")

    # Not in the example XLS, but perhaps should be as it would capture
    # the yearly percentage increase of the negotiated rate
    escalation_rate = models.DecimalField(
        help_text="Escalation Rate"
    )

    commercial_price_per_hour = models.DecimalField(
        help_text="Commercial Price per Hour"
    )
    most_favored_customer = models.CharField(
        help_text="Most Favored Customer Name"
    )

    mfc_discount = models.DecimalField(
        help_text="Most Favored Customer Discount (Percent)"
    )
    mfc_price_per_hour = models.DecimalField(
        help_text="Most Favored Customer Price per Hour"
    )

    gsa_commercial_discount = models.DecimalField(
        help_text="Discount to GSA off of Commercial Rate (Percent)"
    )
    gsa_mfc_discount = models.DecimalField(
        help_text="Discount to GSA off of Most Favored Customer Rate (Percent)"
    )

    # This might be the only price field necessary to keep for CALC's purpose
    gsa_price_per_hour = models.DecimalField(
        help_text="Price offered to GSA"
    )

    supporting_document_number = models.CharField(
        help_text="Support Document Number"
    )

    # PriceList has many PriceListRows
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE)
