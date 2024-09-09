from rest_framework.urls import path

from .views import PaymentTypeList, PaymentTypeDetail, ChargeTypeList, ChargeTypeDetail, ChargeList, ChargeDetail, \
    PaymentList, PaymentDetail, get_monthly_revenue, get_termly_revenue, get_payments_list, get_organization_invoices, \
    get_all_invoices, pay_invoice

urlpatterns = [
    path('payment-types', PaymentTypeList.as_view(), name='payment_type_list'),
    path('payment-types/<int:pk>', PaymentTypeDetail.as_view(), name='payment_type_detail'),

    path('charge-types', ChargeTypeList.as_view(), name='charge_type_list'),
    path('charge-types/<int:pk>', ChargeTypeDetail.as_view(), name='charge_type_detail'),

    path('charge', ChargeList.as_view(), name='charge_list'),
    path('charge/<int:pk>', ChargeDetail.as_view(), name='charge_detail'),

    path('payments', PaymentList.as_view(), name='payment_list'),
    path('payments/<int:pk>', PaymentDetail.as_view(), name='payment_detail'),

    path('bursar/get-monthly-revenue', get_monthly_revenue, name='get_monthly_revenue'),
    path('bursar/get-termly-revenue', get_termly_revenue, name='get_term_revenue'),
    path('bursar/get-payments-list', get_payments_list, name='get_payments_list'),

    path('invoices/organization', get_organization_invoices, name='get_organization_invoices'),
    path('invoices/all', get_all_invoices, name='get_all_invoices'),
    path('invoices/pay', pay_invoice, name='pay_invoice')
]
