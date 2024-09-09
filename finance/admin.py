from django.contrib import admin

from .models.charge_types import ChargeType
from .models.invoices import Invoice
from .models.payments import Payment

admin.site.register(ChargeType)
admin.site.register(Invoice)
admin.site.register(Payment)