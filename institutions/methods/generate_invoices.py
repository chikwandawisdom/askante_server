from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.utils import timezone

from finance.models.invoices import Invoice
from institutions.models.organization import Organization


def generate_invoices():
    current_date = timezone.now().date()

    print('inside generate_invoices: ', current_date)

    organization_with_next_payment_date_as_today = Organization.objects.filter(
        Q(next_payment_date=current_date)
        & ~Q(last_invoice_generated=current_date)
    )

    for organization in organization_with_next_payment_date_as_today:
        print('Creating invoice for ', organization.name)
        Invoice.objects.create(
            organization=organization,
            amount=organization.payment_amount,
            date=current_date
        )

        organization.last_invoice_generated = current_date
        organization.next_payment_date = current_date + relativedelta(months=organization.payment_frequency)
        organization.save()
