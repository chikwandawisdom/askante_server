from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from nanoid import generate

from fundamentals.common_queries import search_by_names, filter_by_institution, search_student_by_name
from fundamentals.custom_responses import success_w_data, err_forbidden, err_w_serializer, err_w_msg, \
    get_paginated_response
from fundamentals.email import send_email
from institutions.models.institution import Institution
from .models.students import Student, StudentWriteSerializer, StudentReadSerializer
from .models.parents import Parent, ParentWriteSerializer, ParentReadSerializer
from .models.student_contacts import StudentContact, StudentContactWriteSerializer, StudentContactReadSerializer
from .models.student_addresses import StudentAddress, StudentAddressWriteSerializer, StudentAddressReadSerializer
from .models.student_types import StudentType, StudentTypeSerializer
from .queries import filter_by_student_id, filter_by_grade, filter_parents_by_student_id,filter_by_student_type, \
    filter_by_gender


class StudentList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data.copy()

        try:
            institution = Institution.objects.get(id=data['institution'])
            data['invitation_code'] = generate()
            if institution.organization != request.user.organization:
                return err_forbidden()
        except KeyError:
            return err_w_msg('institution is required')

        serializer = StudentWriteSerializer(data=data)
        if serializer.is_valid():
            student = serializer.save()
            send_email(to=student.email, subject='School Management System Registration Link', body_params={
                'registration_url': f'https://askante.net/register?code={student.invitation_code}&type=student'
            })
            return success_w_data(serializer.data, status=HTTP_201_CREATED)

        return err_w_serializer(serializer.errors)

    @staticmethod
    def get(request):
        params = request.query_params

        queryset = Student.objects.filter(
            Q(institution__organization=request.user.organization)
            & Q(search_student_by_name(params.get('search'),))
            & filter_by_student_type(params.get('student_type'))
            & filter_by_gender(params.get('gender'))
            & filter_by_institution(params.get('institution'))
            & filter_by_grade(params.get('grade'))
        ).order_by('-id')

        return get_paginated_response(request, queryset, StudentReadSerializer)
 

class StudentDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        try:
            student = Student.objects.get(id=pk)
            if student.institution.organization != request.user.organization:
                return err_forbidden()
        except Student.DoesNotExist:
            return err_w_msg('Student not found')

        serializer = StudentReadSerializer(student)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        try:
            student = Student.objects.get(id=pk)
            if student.institution.organization != request.user.organization:
                return err_forbidden()
        except Student.DoesNotExist:
            return err_w_msg('Student not found')

        serializer = StudentWriteSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)

        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        try:
            student = Student.objects.get(id=pk)
            if student.institution.organization != request.user.organization:
                return err_forbidden()
        except Student.DoesNotExist:
            return err_w_msg('Student not found')

        student.delete()
        return success_w_data('Student deleted')


class ParentListView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data.copy()

        try:
            student = Student.objects.get(id=data['student'])
            if student.institution.organization != request.user.organization:
                return err_forbidden()
        except KeyError:
            return err_w_msg('student is required')

        serializer = ParentWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=HTTP_201_CREATED)

        return err_w_serializer(serializer.errors)

    @staticmethod
    def get(request):
        params = request.query_params

        queryset = Parent.objects.filter(
            Q(student__institution__organization=request.user.organization)
            & Q(search_by_names(params.get('first_name'), params.get('last_name')))
            & filter_by_institution(params.get('institution'))
            & filter_parents_by_student_id(params.get('student'))
        ).order_by('-id')

        return get_paginated_response(request, queryset, ParentReadSerializer)


class ParentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        try:
            parent = Parent.objects.get(id=pk)
            if parent.student.institution.organization != request.user.organization:
                return err_forbidden()
        except Parent.DoesNotExist:
            return err_w_msg('Parent not found')

        serializer = ParentReadSerializer(parent)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        try:
            parent = Parent.objects.get(id=pk)
            if parent.student.institution.organization != request.user.organization:
                return err_forbidden()
        except Parent.DoesNotExist:
            return err_w_msg('Parent not found')

        serializer = ParentWriteSerializer(parent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)

        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        try:
            parent = Parent.objects.get(id=pk)
            if parent.student.institution.organization != request.user.organization:
                return err_forbidden()
        except Parent.DoesNotExist:
            return err_w_msg('Parent not found')

        parent.delete()
        return success_w_data('Parent deleted')


class StudentContactList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data.copy()

        try:
            student = Student.objects.get(id=data['student'])
            if student.institution.organization != request.user.organization:
                return err_forbidden()
        except KeyError:
            return err_w_msg('student is required')

        serializer = StudentContactWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=HTTP_201_CREATED)

        return err_w_serializer(serializer.errors)

    @staticmethod
    def get(request):
        params = request.query_params

        if not params.get('student_id'):
            return err_w_msg('Student ID is required')

        student = Student.objects.filter(id=params.get('student_id'),
                                         institution__organization=request.user.organization.id).first()

        if not student:
            return err_w_msg('Student not found')

        contacts = StudentContact.objects.filter(student=student)

        serializer = StudentContactReadSerializer(contacts, many=True)
        return success_w_data(serializer.data)


class StudentContactDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        try:
            contact = StudentContact.objects.get(id=pk)
            if contact.student.institution.organization != request.user.organization:
                return err_forbidden()
        except StudentContact.DoesNotExist:
            return err_w_msg('Contact not found')

        serializer = StudentContactReadSerializer(contact)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        try:
            contact = StudentContact.objects.get(id=pk)
            if contact.student.institution.organization != request.user.organization:
                return err_forbidden()
        except StudentContact.DoesNotExist:
            return err_w_msg('Contact not found')

        serializer = StudentContactWriteSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)

        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        try:
            contact = StudentContact.objects.get(id=pk)
            if contact.student.institution.organization != request.user.organization:
                return err_forbidden()
        except StudentContact.DoesNotExist:
            return err_w_msg('Contact not found')

        contact.delete()
        return success_w_data('Contact deleted')


class StudentAddressList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data.copy()

        try:
            student = Student.objects.get(id=data['student'])
            if student.institution.organization != request.user.organization:
                return err_forbidden()
        except KeyError:
            return err_w_msg('student is required')

        serializer = StudentAddressWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=HTTP_201_CREATED)

        return err_w_serializer(serializer.errors)

    @staticmethod
    def get(request):
        params = request.query_params

        if not params.get('student_id'):
            return err_w_msg('Student ID is required')

        student = Student.objects.filter(id=params.get('student_id'),
                                         institution__organization=request.user.organization.id).first()

        if not student:
            return err_w_msg('Student not found')

        addresses = StudentAddress.objects.filter(student=student)

        serializer = StudentAddressReadSerializer(addresses, many=True)
        return success_w_data(serializer.data)


class StudentAddressDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        try:
            address = StudentAddress.objects.get(id=pk)
            if address.student.institution.organization != request.user.organization:
                return err_forbidden()
        except StudentAddress.DoesNotExist:
            return err_w_msg('Address not found')

        serializer = StudentAddressReadSerializer(address)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        try:
            address = StudentAddress.objects.get(id=pk)
            if address.student.institution.organization != request.user.organization:
                return err_forbidden()
        except StudentAddress.DoesNotExist:
            return err_w_msg('Address not found')

        serializer = StudentAddressWriteSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)

        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        try:
            address = StudentAddress.objects.get(id=pk)
            if address.student.institution.organization != request.user.organization:
                return err_forbidden()
        except StudentAddress.DoesNotExist:
            return err_w_msg('Address not found')

        address.delete()
        return success_w_data('Address deleted')


class StudentTypeList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        queryset = StudentType.objects.all()
        serializer = StudentTypeSerializer(queryset, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = StudentTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=HTTP_201_CREATED)

        return err_w_serializer(serializer.errors)


class StudentTypeDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        try:
            student_type = StudentType.objects.get(id=pk)
        except StudentType.DoesNotExist:
            return err_w_msg('Student Type not found')

        serializer = StudentTypeSerializer(student_type)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        try:
            student_type = StudentType.objects.get(id=pk)
        except StudentType.DoesNotExist:
            return err_w_msg('Student Type not found')

        serializer = StudentTypeSerializer(student_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)

        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        try:
            student_type = StudentType.objects.get(id=pk)
        except StudentType.DoesNotExist:
            return err_w_msg('Student Type not found')

        student_type.delete()
        return success_w_data('Student Type deleted')
