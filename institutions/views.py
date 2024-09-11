from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from employees.models.employees import Employee
from finance.models.invoices import Invoice, InvoicesReadSerializer
from fundamentals.common_queries import search_by_name, filter_by_institution
from fundamentals.custom_responses import success_w_msg, success_w_data, err_w_serializer, get_paginated_response, \
    err_w_msg
from students.models.students import Student, StudentReadSerializer
from users.permissions import IsSuperUser
from users.serializers import UserRegistrationSerializer
from .models.institution import Institution
from .models.organization import Organization, OrganizationReadSerializer, OrganizationWriteSerializer
from .models.timetables import PeriodWriteSerializer, Period, PeriodReadSerializer
from .serializers import InstitutionWriteSerializer, InstitutionReadSerializer
from .models.grades import Grade, GradeWriteSerializer, GradeReadSerializer
from .models.levels import Level, LevelWriteSerializer, LevelReadSerializer
from .models.subjects import Subject, SubjectWriteSerializer, SubjectReadSerializer
from .models.classes import Class, ClassWriteSerializer, ClassReadSerializer, filter_by_grade
from .models.class_subjects import ClassSubject, ClassSubjectWriteSerializer, ClassSubjectReadSerializer
from .models.academic_years import AcademicYear, AcademicYearWriteSerializer, AcademicYearReadSerializer
from .models.terms import Terms, TermsWriteSerializer, TermsReadSerializer
from .models.room import Room, RoomWriteSerializer, RoomReadSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperUser])
def create_organization(request):
    data = request.data.copy()

    payment_frequency_in_months = data.get('payment_frequency')
    next_payment_date = (timezone.now() + timezone.timedelta(days=payment_frequency_in_months * 30)).date()
    data['next_payment_date'] = next_payment_date

    serializer = OrganizationWriteSerializer(data=data)
    if serializer.is_valid():
        organization = serializer.save()

        data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'username': data['username'],
            'email': data['email'],
            'password': data['password'],
            'organization': organization.id,
            'role': 'admin'
        }

        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.organization = organization
            user.save()

            # create the first invoice
            Invoice.objects.create(organization=organization, amount=organization.payment_amount, date=timezone.now())
        else:
            # delete the organization if the user creation fails
            organization.delete()
            return err_w_serializer(serializer.errors)

        return success_w_data(data={
            'organization': organization.id,
        })
    return success_w_msg(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperUser])
def create_organization_admin(request):
    
    data = request.data.copy()
    data = {
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'username': data['username'],
        'email': data['email'],
        'password': data['password'],
        'organization': data['organization'],
        'role': 'admin'
    }

    organization = Organization.objects.filter(pk=data['organization']).first()
    serializer = UserRegistrationSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        user.organization = organization
        user.save()

        return success_w_msg('Institution admin created successfully.')
    return success_w_msg(serializer.errors)


def filter_by_name(name):
    if name is None:
        return Q()
    return Q(name__icontains=name)


def filter_org_by_district(district):
    if district is None:
        return Q()
    return Q(institutions__district__icontains=district)


def filter_org_by_province(province):
    if province is None:
        return Q()
    return Q(institutions__province__icontains=province)


def filter_org_by_type(type):
    if type is None:
        return Q()
    return Q(institutions__type__icontains=type)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSuperUser])
def get_organizations(request):
    organizations = Organization.objects.filter(
        filter_by_name(request.query_params.get('search'))
        & filter_org_by_district(request.query_params.get('district'))
        & filter_org_by_province(request.query_params.get('province'))
        & filter_org_by_type(request.query_params.get('type'))
    ).order_by('-updated_at')
    serializer = OrganizationReadSerializer(organizations, many=True)
    return success_w_data(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsSuperUser])
def update_organization(request, pk):
    organization = Organization.objects.filter(pk=pk).first()

    if not organization:
        return success_w_msg('Organization not found.', status=HTTP_404_NOT_FOUND)

    data = request.data.copy()

    serializer = OrganizationWriteSerializer(organization, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return success_w_data(serializer.data)
    return err_w_serializer(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_institution(request):
    data = request.data.copy()
    #
    # # Add organization to the data
    # data['organization'] = request.user.organization.id

    serializer = InstitutionWriteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return success_w_msg('Institution created successfully.')
    return success_w_msg(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_institutions(request):
    organization = request.user.organization

    if request.user.is_superuser:
        institutions = Institution.objects.filter(
            filter_by_name(request.query_params.get('search'))
        )
    else:
        institutions = Institution.objects.filter(organization=organization)

    serializer = InstitutionReadSerializer(institutions, many=True)
    return success_w_msg(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsSuperUser])
def edit_institution(request, pk):
    institution = Institution.objects.filter(pk=pk).first()

    if not institution:
        return success_w_msg('Institution not found.', status=HTTP_404_NOT_FOUND)

    data = request.data.copy()

    serializer = InstitutionWriteSerializer(institution, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return success_w_data(serializer.data)
    return err_w_serializer(serializer.errors)


class LevelList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        levels = Level.objects.filter(
            search_by_name(request.query_params.get('search'))
        ).order_by('-id')
        serializer = LevelReadSerializer(levels, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = LevelWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=201)
        return err_w_serializer(serializer.errors)


class LevelDetails(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        level = Level.objects.filter(pk=pk).first()

        if not level:
            return success_w_msg('Level not found.', status=HTTP_404_NOT_FOUND)

        serializer = LevelReadSerializer(level)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        level = Level.objects.filter(pk=pk).first()

        if not level:
            return success_w_msg('Level not found.', status=HTTP_404_NOT_FOUND)

        data = request.data.copy()

        serializer = LevelWriteSerializer(level, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        level = Level.objects.filter(pk=pk).first()

        if not level:
            return success_w_msg('Level not found.', status=HTTP_404_NOT_FOUND)

        level.delete()
        return success_w_msg('Level deleted successfully.')


class GradeList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        grades = Grade.objects.filter(
            search_by_name(request.query_params.get('search'))
        ).order_by('-id')
        serializer = GradeReadSerializer(grades, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = GradeWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=201)
        return err_w_serializer(serializer.errors)


class GradeView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        grade = Grade.objects.filter(pk=pk).first()

        if not grade:
            return success_w_msg('Grade not found.', status=HTTP_404_NOT_FOUND)

        serializer = GradeReadSerializer(grade)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        grade = Grade.objects.filter(pk=pk).first()

        if not grade:
            return success_w_msg('Grade not found.', status=HTTP_404_NOT_FOUND)

        data = request.data.copy()

        serializer = GradeWriteSerializer(grade, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)


class SubjectList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        subjects = Subject.objects.filter(
            search_by_name(request.query_params.get('search'))
        ).order_by('-id')
        serializer = SubjectReadSerializer(subjects, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = SubjectWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=201)
        return err_w_serializer(serializer.errors)


class SubjectDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        subject = Subject.objects.filter(pk=pk).first()

        if not subject:
            return success_w_msg('Subject not found.', status=HTTP_404_NOT_FOUND)

        serializer = SubjectReadSerializer(subject)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        subject = Subject.objects.filter(pk=pk).first()

        if not subject:
            return success_w_msg('Subject not found.', status=HTTP_404_NOT_FOUND)

        data = request.data.copy()

        serializer = SubjectWriteSerializer(subject, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        subject = Subject.objects.filter(pk=pk).first()

        if not subject:
            return success_w_msg('Subject not found.', status=HTTP_404_NOT_FOUND)

        subject.delete()
        return success_w_msg('Subject deleted successfully.')


class ClassList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        classes = Class.objects.filter(
            Q(institution__organization=request.user.organization)
            & search_by_name(request.query_params.get('search'))
            & filter_by_institution(request.query_params.get('institution'))
            & filter_by_grade(request.query_params.get('grade'))
        ).order_by('-id')
        serializer = ClassReadSerializer(classes, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = ClassWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=201)
        return err_w_serializer(serializer.errors)


class ClassDetails(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        class_ = Class.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not class_:
            return success_w_msg('Class not found.', status=HTTP_404_NOT_FOUND)

        serializer = ClassReadSerializer(class_)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        class_ = Class.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not class_:
            return success_w_msg('Class not found.', status=HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['institution'] = class_.institution.id

        if data.get('class_teacher'):
            teacher = Employee.objects.filter(pk=data.get('class_teacher')).first()
            if not teacher:
                return success_w_msg('Teacher not found.', status=HTTP_404_NOT_FOUND)

            try:
                if teacher.is_teacher is False:
                    return success_w_msg('Employee is not a teacher.', status=HTTP_400_BAD_REQUEST)
            except AttributeError:
                return success_w_msg('Employee is not a teacher.', status=HTTP_400_BAD_REQUEST)

        serializer = ClassWriteSerializer(class_, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        class_ = Class.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not class_:
            return success_w_msg('Class not found.', status=HTTP_404_NOT_FOUND)

        class_.delete()
        return success_w_msg('Class deleted successfully.')


class ClassSubjectList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        params = request.query_params

        if params.get('_class') is None:
            return success_w_msg('_class is required.')

        class_subjects = ClassSubject.objects.filter(
            Q(institution__organization=request.user.organization)
            & Q(_class=params.get('_class'))
        ).order_by('-id')
        serializer = ClassSubjectReadSerializer(class_subjects, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = ClassSubjectWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=201)
        return err_w_serializer(serializer.errors)


class ClassSubjectDetails(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        class_subject = ClassSubject.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not class_subject:
            return success_w_msg('ClassSubject not found.', status=HTTP_404_NOT_FOUND)

        serializer = ClassSubjectReadSerializer(class_subject)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        class_subject = ClassSubject.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not class_subject:
            return success_w_msg('ClassSubject not found.', status=HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['institution'] = class_subject.institution.id

        if data.get('teacher'):
            teacher = Employee.objects.filter(pk=data.get('teacher')).first()
            if not teacher:
                return success_w_msg('Teacher not found.', status=HTTP_404_NOT_FOUND)

            try:
                if teacher.is_teacher is False:
                    return err_w_msg('Employee is not a teacher.', status=HTTP_400_BAD_REQUEST)
            except AttributeError:
                return err_w_msg('Employee is not a teacher.', status=HTTP_400_BAD_REQUEST)

        serializer = ClassSubjectWriteSerializer(class_subject, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        class_subject = ClassSubject.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not class_subject:
            return success_w_msg('ClassSubject not found.', status=HTTP_404_NOT_FOUND)

        class_subject.delete()
        return success_w_msg('ClassSubject deleted successfully.')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_students_to_class(request):
    data = request.data.copy()

    _class = Class.objects.filter(pk=data['_class'], institution__organization=request.user.organization).first()
    if not _class:
        return success_w_msg('Class not found.', status=HTTP_404_NOT_FOUND)

    students = data.get('students')

    # add students to class
    _class.students.add(*students)

    return success_w_msg('Students added to class successfully.')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_students_in_class(request):
    _class_id = request.query_params.get('_class')
    _class = Class.objects.filter(pk=_class_id, institution__organization=request.user.organization).first()

    if not _class:
        return success_w_msg('Class not found.', status=HTTP_404_NOT_FOUND)

    students = _class.students.all()
    serializer = StudentReadSerializer(students, many=True)
    return success_w_data(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_student_from_class(request):
    data = request.data.copy()

    try:
        _class = Class.objects.filter(pk=data['_class'], institution__organization=request.user.organization).first()
        if not _class:
            return success_w_msg('Class not found.', status=HTTP_404_NOT_FOUND)

        student = data['student']

        # remove students from class
        _class.students.remove(student)

    except KeyError:
        return success_w_msg('_class is required.')

    return success_w_msg('Student removed from class successfully.')


class AcademicYearList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        academic_years = AcademicYear.objects.filter(
            Q(institution__organization=request.user.organization)
            & search_by_name(request.query_params.get('search'))
            & filter_by_institution(request.query_params.get('institution'))
        ).order_by('-id')
        serializer = AcademicYearReadSerializer(academic_years, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()

        institution = Institution.objects.filter(pk=data['institution'], organization=request.user.organization).first()
        if not institution:
            return success_w_msg('Institution not found.', status=HTTP_404_NOT_FOUND)

        serializer = AcademicYearWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=201)
        return err_w_serializer(serializer.errors)


class AcademicYearDetails(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        academic_year = AcademicYear.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not academic_year:
            return success_w_msg('AcademicYear not found.', status=HTTP_404_NOT_FOUND)

        serializer = AcademicYearReadSerializer(academic_year)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        academic_year = AcademicYear.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not academic_year:
            return success_w_msg('AcademicYear not found.', status=HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['institution'] = academic_year.institution.id

        serializer = AcademicYearWriteSerializer(academic_year, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        academic_year = AcademicYear.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not academic_year:
            return success_w_msg('AcademicYear not found.', status=HTTP_404_NOT_FOUND)

        academic_year.delete()
        return success_w_msg('AcademicYear deleted successfully.')


class TermsList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        terms = Terms.objects.filter(
            search_by_name(request.query_params.get('search'))
        ).order_by('-id')
        serializer = TermsReadSerializer(terms, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = TermsWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=201)
        return err_w_serializer(serializer.errors)


class TermsDetails(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        term = Terms.objects.filter(pk=pk).first()

        if not term:
            return success_w_msg('Term not found.', status=HTTP_404_NOT_FOUND)

        serializer = TermsReadSerializer(term)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        term = Terms.objects.filter(pk=pk).first()

        if not term:
            return success_w_msg('Term not found.', status=HTTP_404_NOT_FOUND)

        data = request.data.copy()

        serializer = TermsWriteSerializer(term, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        term = Terms.objects.filter(pk=pk).first()

        if not term:
            return success_w_msg('Term not found.', status=HTTP_404_NOT_FOUND)

        term.delete()
        return success_w_msg('Term deleted successfully.')


class RoomList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        rooms = Room.objects.filter(
            Q(institution__organization=request.user.organization)
            & search_by_name(request.query_params.get('search'))
            & filter_by_institution(request.query_params.get('institution'))
        ).order_by('-id')
        serializer = RoomReadSerializer(rooms, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()

        institution = Institution.objects.filter(pk=data['institution'], organization=request.user.organization).first()
        if not institution:
            return success_w_msg('Institution not found.', status=HTTP_404_NOT_FOUND)

        serializer = RoomWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=201)
        return err_w_serializer(serializer.errors)


class RoomDetails(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        room = Room.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not room:
            return success_w_msg('Room not found.', status=HTTP_404_NOT_FOUND)

        serializer = RoomReadSerializer(room)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        room = Room.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not room:
            return success_w_msg('Room not found.', status=HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['institution'] = room.institution.id

        serializer = RoomWriteSerializer(room, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        room = Room.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not room:
            return success_w_msg('Room not found.', status=HTTP_404_NOT_FOUND)

        room.delete()
        return success_w_msg('Room deleted successfully.')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_period(request):
    data = request.data.copy()

    class_subject = ClassSubject.objects.filter(pk=data['class_subject'],
                                                institution__organization=request.user.organization).first()
    if not class_subject:
        return success_w_msg('ClassSubject not found.', status=HTTP_404_NOT_FOUND)

    serializer = PeriodWriteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return success_w_data(serializer.data, status=201)
    return err_w_serializer(serializer.errors)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_period(request, pk):
    period = Period.objects.filter(pk=pk).first()

    if not period:
        return success_w_msg('Period not found.', status=HTTP_404_NOT_FOUND)

    data = request.data.copy()

    serializer = PeriodWriteSerializer(period, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return success_w_data(serializer.data)
    return err_w_serializer(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_periods_of_a_class(request):
    _class = request.query_params.get('_class')
    if _class is None:
        return success_w_msg('_class is required.')

    _class = Class.objects.filter(id=_class, institution__organization=request.user.organization).first()

    print(_class)

    if _class is None:
        return success_w_msg('Class not found.', status=HTTP_404_NOT_FOUND)

    periods = Period.objects.select_related('class_subject').filter(class_subject___class=_class)
    periods = PeriodReadSerializer(periods, many=True)

    return success_w_data(periods.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_period(request, pk):
    period = Period.objects.filter(pk=pk, class_subject__institution__organization=request.user.organization).first()

    if not period:
        return success_w_msg('Period not found.', status=HTTP_404_NOT_FOUND)

    period.delete()
    return success_w_msg('Period deleted successfully.')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_academic_year(request):
    data = request.data.copy()

    academic_year = AcademicYear.objects.filter(pk=data['academic_year'],
                                                institution__organization=request.user.organization).first()
    if not academic_year:
        return success_w_msg('AcademicYear not found.', status=HTTP_404_NOT_FOUND)

    current_active_academic_year = AcademicYear.objects.filter(institution=academic_year.institution,
                                                               is_active=True).first()
    if current_active_academic_year:
        current_active_academic_year.is_active = False
        current_active_academic_year.save()

    academic_year.is_active = True
    academic_year.save()

    return success_w_msg('Academic year changed successfully.')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invoices(request):
    if request.user.is_superuser:
        queryset = Invoice.objects.all().order_by('-id')
    else:
        queryset = Invoice.objects.filter(organization=request.user.organization).order_by('-id')

    return get_paginated_response(queryset=queryset, request=request, serializer=InvoicesReadSerializer)
