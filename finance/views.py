import requests
import calendar
import os
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import APIView, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from fundamentals.custom_responses import success_w_msg, err_w_serializer, success_w_data, get_paginated_response, \
    err_w_msg
from institutions.models.terms import Terms
from users.permissions import IsBursar, IsSuperUser
from .models.charge_types import ChargeType, ChargeTypeWriteSerializer, ChargeTypeReadSerializer
from .models.charges import Charge, ChargeWriteSerializer, ChargeReadSerializer
from .models.invoices import Invoice, InvoicesReadSerializer
from .models.payment_types import PaymentType, PaymentTypeWriteSerializer, PaymentTypeReadSerializer
from .models.payments import (Payment, PaymentWriteSerializer, PaymentReadSerializer, filter_by_institution,
                              filter_by_student, filter_by_date_range)


class PaymentTypeList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = PaymentTypeWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg('Payment type created successfully')
        return err_w_serializer(serializer.errors)

    @staticmethod
    def get(request):
        organization = request.user.organization
        payment_types = PaymentType.objects.filter().order_by('name')
        serializer = PaymentTypeReadSerializer(payment_types, many=True)
        return success_w_data(serializer.data)


class PaymentTypeDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        try:
            payment_type = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeReadSerializer(payment_type)
            return success_w_data(serializer.data)
        except PaymentType.DoesNotExist:
            return err_w_serializer('Payment type not found')

    @staticmethod
    def patch(request, pk):
        try:
            payment_type = PaymentType.objects.filter(pk=pk).first()

            data = request.data.copy()
            data['organization'] = request.user.organization.id

            serializer = PaymentTypeWriteSerializer(payment_type, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_w_msg('Payment type updated successfully')
            return err_w_serializer(serializer.errors)
        except PaymentType.DoesNotExist:
            return err_w_serializer('Payment type not found')

    @staticmethod
    def delete(request, pk):
        try:
            payment_type = PaymentType.objects.filter(pk=pk).first()
            payment_type.delete()
            return success_w_msg('Payment type deleted successfully')
        except PaymentType.DoesNotExist:
            return err_w_serializer('Payment type not found')


class ChargeTypeList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = ChargeTypeWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg('Charge type created successfully')
        return err_w_serializer(serializer.errors)

    @staticmethod
    def get(request):
        organization = request.user.organization
        charge_types = ChargeType.objects.filter().order_by('name')
        serializer = ChargeTypeReadSerializer(charge_types, many=True)
        return success_w_data(serializer.data)


class ChargeTypeDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        try:
            charge_type = ChargeType.objects.get(pk=pk)
            serializer = ChargeTypeReadSerializer(charge_type)
            return success_w_data(serializer.data)
        except ChargeType.DoesNotExist:
            return err_w_serializer('Charge type not found')

    @staticmethod
    def patch(request, pk):
        try:
            charge_type = ChargeType.objects.filter(pk=pk).first()

            data = request.data.copy()

            serializer = ChargeTypeWriteSerializer(charge_type, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_w_msg('Charge type updated successfully')
            return err_w_serializer(serializer.errors)
        except ChargeType.DoesNotExist:
            return err_w_serializer('Charge type not found')

    @staticmethod
    def delete(request, pk):
        try:
            charge_type = ChargeType.objects.filter(pk=pk).first()
            charge_type.delete()
            return success_w_msg('Charge type deleted successfully')
        except ChargeType.DoesNotExist:
            return err_w_serializer('Charge type not found')


class ChargeList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data.copy()
        data['organization'] = request.user.organization.id

        serializer = ChargeWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg('Charge created successfully')
        return err_w_serializer(serializer.errors)

    @staticmethod
    def get(request):
        organization = request.user.organization
        charges = Charge.objects.filter(organization=organization).order_by('name')
        serializer = ChargeReadSerializer(charges, many=True)
        return success_w_data(serializer.data)


class ChargeDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        try:
            charge = Charge.objects.get(pk=pk)
            serializer = ChargeReadSerializer(charge)
            return success_w_data(serializer.data)
        except Charge.DoesNotExist:
            return err_w_serializer('Charge not found')

    @staticmethod
    def patch(request, pk):
        try:
            charge = Charge.objects.filter(pk=pk, organization=request.user.organization).first()

            data = request.data.copy()
            data['organization'] = request.user.organization.id

            serializer = ChargeWriteSerializer(charge, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_w_msg('Charge updated successfully')
            return err_w_serializer(serializer.errors)
        except Charge.DoesNotExist:
            return err_w_serializer('Charge not found')

    @staticmethod
    def delete(request, pk):
        try:
            charge = Charge.objects.filter(pk=pk, organization=request.user.organization).first()
            charge.delete()
            return success_w_msg('Charge deleted successfully')
        except Charge.DoesNotExist:
            return err_w_serializer('Charge not found')


class PaymentList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data.copy()
        data['organization'] = request.user.organization.id

        serializer = PaymentWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg('Payment created successfully')
        return err_w_serializer(serializer.errors)

    @staticmethod
    def get(request):
        params = request.query_params
        organization = request.user.organization
        payments = Payment.objects.filter(
            Q(organization=organization)
            & filter_by_student(params.get('student'))
            & filter_by_institution(params.get('institution'))
            & filter_by_date_range(params.get('start'), params.get('end'))
        ).order_by('-id')
        return get_paginated_response(request, payments, PaymentReadSerializer)


class PaymentDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        try:
            payment = Payment.objects.filter(pk=pk, organization=request.user.organization).first()
            serializer = PaymentReadSerializer(payment)
            return success_w_data(serializer.data)
        except Payment.DoesNotExist:
            return err_w_serializer('Payment not found')

    @staticmethod
    def patch(request, pk):
        try:
            payment = Payment.objects.filter(pk=pk, organization=request.user.organization).first()

            data = request.data.copy()
            data['organization'] = request.user.organization.id

            serializer = PaymentWriteSerializer(payment, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_w_msg('Payment updated successfully')
            return err_w_serializer(serializer.errors)
        except Payment.DoesNotExist:
            return err_w_serializer('Payment not found')


# display revenue for the month for the users organization


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsBursar])
def get_monthly_revenue(request):
    organization = request.user.organization
    today = timezone.now()
    current_year = today.year
    monthly_revenue = {}

    for month in range(1, 13):
        start_of_month = timezone.datetime(current_year, month, 1)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        payments = Payment.objects.filter(
            Q(organization=organization)
            & filter_by_date_range(start_of_month.strftime('%Y-%m-%d'), end_of_month.strftime('%Y-%m-%d'))
        )
        total = sum([payment.amount for payment in payments])
        month_name = calendar.month_name[month]
        monthly_revenue[month_name] = total

    return success_w_data(monthly_revenue)


# get revenue for each term for the users organization to show in a pie chart
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsBursar])
def get_termly_revenue(request):
    organization = request.user.organization
    term_revenue = {}

    terms = Terms.objects.all()
    if not terms.exists():
        return success_w_data(None)

    for term in terms:
        payments = Payment.objects.filter(
            Q(organization=organization)
            & Q(term=term)
        )
        total = sum([payment.amount for payment in payments])
        term_name = term.name
        term_revenue[term_name] = total

    return success_w_data(term_revenue)


# filter payments based on charge type and term and send the array
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsBursar])
def get_payments_list(request):
    organization = request.user.organization
    params = request.query_params
    charge_type_pk = params.get('charge_type')
    term_pk = params.get('term')

    filters = Q(organization=organization)
    if charge_type_pk:
        charge_type_pk = int(charge_type_pk)
        filters &= Q(charges__contains=[{'charge_type': {'id': charge_type_pk}}])
    if term_pk:
        filters &= Q(term_id=term_pk)

    payments = Payment.objects.filter(filters)

    filtered_payments = []
    for payment in payments:
        if charge_type_pk:
            filtered_charges = [charge for charge in payment.charges if charge['charge_type']['id'] == charge_type_pk]
        else:
            filtered_charges = payment.charges
        if filtered_charges:
            payment_data = PaymentReadSerializer(payment).data
            payment_data['charges'] = filtered_charges
            filtered_payments.append(payment_data)

    return success_w_data(data=filtered_payments)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organization_invoices(request):
    organization = request.user.organization
    queryset = Invoice.objects.select_related('organization').filter(organization=organization).order_by('-id')

    return get_paginated_response(request, queryset, InvoicesReadSerializer)


def filter_invoice_by_organization(organization):
    if organization is None:
        return Q()
    return Q(organization=organization)


def filter_invoice_by_paid_status(is_paid):
    if is_paid is None:
        return Q()
    is_paid = True if is_paid == 'true' else False
    return Q(is_paid=bool(is_paid))


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSuperUser])
def get_all_invoices(request):
    params = request.query_params
    queryset = Invoice.objects.select_related('organization').filter(
        filter_invoice_by_organization(params.get('organization'))
        & filter_invoice_by_paid_status(params.get('is_paid'))
    ).order_by('-id')

    return get_paginated_response(request, queryset, InvoicesReadSerializer)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay_invoice(request):
    data = request.data

    invoice_id = data.get('invoice_id')

    if invoice_id is None:
        return err_w_msg('Invoice id is required')

    invoice = Invoice.objects.filter(id=invoice_id).first()
    if invoice is None:
        return err_w_msg('Invoice not found')

    try:
        yoco_api_url = 'https://online.yoco.com/v1/charges/'
        yoco_secret_key = os.getenv('YOCO_SECRET_KEY', '')

        headers = {
            'X-Auth-Secret-Key': yoco_secret_key,
        }

        response = requests.post(yoco_api_url, json=data, headers=headers)
        response_data = response.json()

        if response.status_code in [200, 201]:

            # Assuming both status codes represent successful payment
            invoice.is_paid = True
            # todo: handle this token
            # invoice.token = data.get('token')
            invoice.save()

            return success_w_msg(msg='Payment successful', )

        elif response.status_code == 400:
            # Add some logs when payment fails
            return Response({'status': 'not ok', 'error': response_data}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'not ok', 'error': response_data}, status=response.status_code)

    except requests.RequestException as error:
        return Response({'status': 'not ok', 'error': str(error)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
