from rest_framework.decorators import APIView, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED
from nanoid import generate
from django.db.models import Q

from fundamentals.custom_responses import success_w_data, err_w_serializer, err_w_msg, success_w_msg, \
    get_paginated_response
from fundamentals.email import send_email
from .models.employees import Employee, EmployeeReadSerializer, EmployeeWriteSerializer
from .models.employment_positions import EmploymentPosition, EmploymentPositionWriteSerializer, \
    EmploymentPositionReadSerializer
from .models.employment_types import EmploymentType, EmploymentTypeWriteSerializer, EmploymentTypeReadSerializer
from .models.employee_addresses import EmployeeAddress, EmployeeAddressWriteSerializer, EmployeeAddressReadSerializer
from .models.employee_contacts import EmployeeContact, EmployeeContactWriteSerializer, EmployeeContactReadSerializer

from .queries import filter_by_gender, search_by_employee_name


class EmploymentPositionList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        positions = EmploymentPosition.objects.filter(organization=request.user.organization.id)
        serializer = EmploymentPositionReadSerializer(positions, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()
        data['organization'] = request.user.organization.id
        serializer = EmploymentPositionWriteSerializer(data=data)
        if serializer.is_valid():
            return success_w_data(data=serializer.data, msg='Employment position created successfully',
                                  status=HTTP_201_CREATED)
        return err_w_serializer(errors=serializer)


class EmploymentPositionDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        position = EmploymentPosition.objects.filter(id=pk, organization=request.user.organization.id).first()

        if not position:
            return err_w_msg('Employment position not found')

        serializer = EmploymentPositionReadSerializer(position)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        data = request.data.copy()
        data['organization'] = request.user.organization.id

        position = EmploymentPosition.objects.filter(id=pk, organization=request.user.organization.id).first()

        if not position:
            return err_w_msg('Employment position not found')

        serializer = EmploymentPositionWriteSerializer(instance=position, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(data=serializer.data, msg='Employment position updated successfully')
        return err_w_serializer(errors=serializer)

    @staticmethod
    def delete(request, pk):
        position = EmploymentPosition.objects.filter(id=pk, organization=request.user.organization.id).first()

        if not position:
            return err_w_msg('Employment position not found')

        position.delete()
        return success_w_msg(msg='Employment position deleted successfully')


class EmploymentTypeList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        types = EmploymentType.objects.filter(organization=request.user.organization.id)
        serializer = EmploymentTypeReadSerializer(types, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()
        print(data)
        data['organization'] = request.user.organization.id
        serializer = EmploymentTypeWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(data=serializer.data, msg='Employment type created successfully',
                                  status=HTTP_201_CREATED)
        return err_w_serializer(errors=serializer)


class EmploymentTypeDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        employment_type = EmploymentType.objects.filter(id=pk, organization=request.user.organization.id).first()

        if not employment_type:
            return err_w_msg('Employment type not found')

        serializer = EmploymentTypeReadSerializer(employment_type)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        data = request.data.copy()
        data['organization'] = request.user.organization.id

        employment_type = EmploymentType.objects.filter(id=pk, organization=request.user.organization.id).first()

        if not employment_type:
            return err_w_msg('Employment type not found')

        serializer = EmploymentTypeWriteSerializer(instance=employment_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(data=serializer.data, msg='Employment type updated successfully')
        return err_w_serializer(errors=serializer)

    @staticmethod
    def delete(request, pk):
        employment_type = EmploymentType.objects.filter(id=pk, organization=request.user.organization.id).first()

        if not employment_type:
            return err_w_msg('Employment type not found')

        employment_type.delete()
        return success_w_msg(msg='Employment type deleted successfully')


class EmployeeList(APIView):
    permission_classes = [IsAuthenticated]

    # @staticmethod
    # def get(request):
    #     # todo: add filter here
    #     queryset = Employee.objects.filter(institution__organization=request.user.organization.id).order_by('-id')
    #     return get_paginated_response(request, queryset, EmployeeReadSerializer)
    

    @staticmethod
    def get(request):
        params = request.query_params

        queryset = Employee.objects.filter(
            Q(institution__organization=request.user.organization)
            & Q(search_by_employee_name(params.get('search'),))
            & filter_by_gender(params.get('gender'))

        ).order_by('-id')

        return get_paginated_response(request, queryset, EmployeeReadSerializer)

    @staticmethod
    def post(request):
        data = request.data.copy()
        print(data)
        data['organization'] = request.user.organization.id
        data['invitation_code'] = generate()
        serializer = EmployeeWriteSerializer(data=data)
        if serializer.is_valid():
            employee = serializer.save()
            send_email(to=employee.email, subject='School Management System Registration Link', body_params={
                'registration_url': f'https://askante.net/register?code={employee.invitation_code}&type=employee'
            })
            return success_w_data(data=serializer.data, msg='Employee created successfully',
                                  status=HTTP_201_CREATED)
        return err_w_serializer(errors=serializer.errors)


class EmployeeDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        employee = Employee.objects.filter(id=pk, institution__organization=request.user.organization.id).first()

        if not employee:
            return err_w_msg('Employee not found')

        serializer = EmployeeReadSerializer(employee)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        data = request.data.copy()
        data['organization'] = request.user.organization.id

        employee = Employee.objects.filter(id=pk, institution__organization=request.user.organization.id).first()

        if not employee:
            return err_w_msg('Employee not found')

        serializer = EmployeeWriteSerializer(instance=employee, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
            except ValidationError as e:
                return err_w_msg(str(e.detail[0]))
            return success_w_data(data=serializer.data, msg='Employee updated successfully')
        return err_w_serializer(errors=serializer.errors)

    @staticmethod
    def delete(request, pk):
        employee = Employee.objects.filter(id=pk, institution__organization=request.user.organization.id).first()

        if not employee:
            return err_w_msg('Employee not found')

        employee.delete()
        return success_w_msg(msg='Employee deleted successfully')


class EmployeeAddressList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        params = request.query_params

        if not params.get('employee_id'):
            return err_w_msg('Employee ID is required')

        employee = Employee.objects.filter(id=params.get('employee_id'),
                                           institution__organization=request.user.organization.id).first()

        if not employee:
            return err_w_msg('Employee not found')

        addresses = EmployeeAddress.objects.filter(employee=employee)

        serializer = EmployeeAddressReadSerializer(addresses, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()
        data['organization'] = request.user.organization.id
        serializer = EmployeeAddressWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(data=serializer.data, msg='Employee address created successfully',
                                  status=HTTP_201_CREATED)
        return err_w_serializer(errors=serializer.errors)


class EmployeeAddressDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        address = EmployeeAddress.objects.filter(id=pk,
                                                 employee__institution__organization=request.user.organization.id).first()

        if not address:
            return err_w_msg('Employee address not found')

        serializer = EmployeeAddressReadSerializer(address)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        data = request.data.copy()
        data['organization'] = request.user.organization.id

        address = EmployeeAddress.objects.filter(id=pk,
                                                 employee__institution__organization=request.user.organization.id).first()

        if not address:
            return err_w_msg('Employee address not found')

        serializer = EmployeeAddressWriteSerializer(instance=address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(data=serializer.data, msg='Employee address updated successfully')
        return err_w_serializer(errors=serializer.errors)

    @staticmethod
    def delete(request, pk):
        address = EmployeeAddress.objects.filter(id=pk,
                                                 employee__institution__organization=request.user.organization.id).first()

        if not address:
            return err_w_msg('Employee address not found')

        address.delete()
        return success_w_msg(msg='Employee address deleted successfully')


class EmployeeContactList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        params = request.query_params

        if not params.get('employee_id'):
            return err_w_msg('Employee ID is required')

        employee = Employee.objects.filter(id=params.get('employee_id'),
                                           institution__organization=request.user.organization.id).first()

        if not employee:
            return err_w_msg('Employee not found')

        contacts = EmployeeContact.objects.filter(employee=employee)

        serializer = EmployeeContactReadSerializer(contacts, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()
        data['organization'] = request.user.organization.id
        serializer = EmployeeContactWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(data=serializer.data, msg='Employee contact created successfully',
                                  status=HTTP_201_CREATED)
        return err_w_serializer(errors=serializer.errors)


class EmployeeContactDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        contact = EmployeeContact.objects.filter(id=pk,
                                                 employee__institution__organization=request.user.organization.id).first()

        if not contact:
            return err_w_msg('Employee contact not found')

        serializer = EmployeeContactReadSerializer(contact)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        data = request.data.copy()
        data['organization'] = request.user.organization.id

        contact = EmployeeContact.objects.filter(id=pk,
                                                 employee__institution__organization=request.user.organization.id).first()

        if not contact:
            return err_w_msg('Employee contact not found')

        serializer = EmployeeContactWriteSerializer(instance=contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(data=serializer.data, msg='Employee contact updated successfully')
        return err_w_serializer(errors=serializer.errors)

    @staticmethod
    def delete(request, pk):
        contact = EmployeeContact.objects.filter(id=pk,
                                                 employee__institution__organization=request.user.organization.id).first()

        if not contact:
            return err_w_msg('Employee contact not found')

        contact.delete()
        return success_w_msg(msg='Employee contact deleted successfully')