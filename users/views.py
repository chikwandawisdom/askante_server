import threading

from django.contrib.auth.models import update_last_login
from django.db.models import Q
from django.utils import timezone
from nanoid import generate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from book_shop.models.publisher_users import PublisherUser
from book_shop.models.publishers import Publisher
from employees.models.employees import Employee
from finance.models.invoices import Invoice, InvoicesReadSerializer
from fundamentals.custom_responses import err_w_msg, success_w_data, get_paginated_response, success_w_msg
from fundamentals.email import send_email
from institutions.methods.generate_invoices import generate_invoices
from students.models.students import Student
from users.auth_utils import access_token_generator
from users.models import User
from users.permissions import IsSuperUser
from users.serializers import UserSerializer, UserRegistrationSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = request.data

    if not data.get('username') or not data.get('password'):
        return err_w_msg('Username and password are required')

    user = User.objects.filter(username=data['username']).first()
    if user is None:
        return err_w_msg('Invalid credentials')

    if not user.check_password(data['password']):
        return err_w_msg('Invalid credentials')

    if user.is_active is False:
        return err_w_msg('User account not activated. Contact your administrator')
    
    # updating user last login
    update_last_login(None, user)
    user_data = UserSerializer(user, many=False).data
    access_token = access_token_generator(user)

    return success_w_data({'user': user_data, 'access_token': access_token}, 'Login successful')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authenticate(request):
    user = request.user

    if user.is_active is False:
        return err_w_msg('User account not activated. Contact your administrator')

    if user.role == 'publisher':
        publisher = Publisher.objects.filter(id=user.publisher).first()
        if publisher.is_active is False:
            return err_w_msg('Publisher account not activated. Contact your administrator')

    if user.role == 'student' or user.role == 'employee':
        if user.organization.is_active is False:
            return err_w_msg('Institution account not activated. Contact your administrator')
    
    # Attach picture to employee
    employee = user.employee_set.values_list('dp').last()
    if employee is not None:
        user.dp = employee[0]

    # Attach picture to student
    student = user.student_user.values_list('dp').last()
    if student is not None:
        user.dp = student[0]

    user_data = UserSerializer(user).data

    # updating user last session
    user.last_session = timezone.now()
    user.save()

    # look for unpaid invoice
    unpaid_invoice = Invoice.objects.filter(organization=user.organization, is_paid=False).first()
    if unpaid_invoice:
        user_data['unpaid_invoice'] = InvoicesReadSerializer(unpaid_invoice).data

    threading.Thread(target=generate_invoices, args=()).start()

    return success_w_data(user_data, 'User authenticated successfully')


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data.copy()
    try:
        type = data.get('type')

        record = None
        if type == 'employee':
            record = Employee.objects.filter(invitation_code=data['invitation_code']).first()
        elif type == 'student':
            record = Student.objects.filter(invitation_code=data['invitation_code']).first()
        elif type == 'publisher':
            record = PublisherUser.objects.filter(invitation_code=data['invitation_code']).first()

        if record is None:
            return err_w_msg('Invalid invitation code')

        duplicate_user = User.objects.filter(username=data['username']).first()
        if duplicate_user:
            return err_w_msg('Username already exists')

        data['first_name'] = record.first_name
        data['last_name'] = record.last_name

        if type == 'employee':
            if record.is_teacher:
                data['role'] = 'teacher'
            else:
                data['role'] = 'employee'
        elif type == 'student':
            data['role'] = 'student'
        elif type == 'publisher':
            data['role'] = 'publisher'

        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            try:
                if record.special_role is not None:
                    user.special_role = record.special_role
                    user.save()
            except Exception as e:
                pass

            user.email = record.email
            if type != 'publisher':
                print('inside institution')
                user.organization = record.institution.organization
                user.dp = record.dp

            if type == 'publisher':
                user.publisher = record.publisher.id

            user.save()

            record.invitation_code = None
            record.user = user
            record.save()

            return success_w_data(serializer.data, 'User registered successfully')
        else:
            return err_w_msg(serializer.errors)

    except Exception as e:
        return err_w_msg(str(e))


def search_users_by_name(search):
    if search is None:
        return Q()
    return Q(first_name__icontains=search) | Q(last_name__icontains=search)


def search_users_by_organization(organization):
    if organization is None:
        return Q()
    return Q(organization=organization)


def filter_student_user_by_grade(grade):
    if grade is None:
        return Q()
    return Q(student_user__grade=grade)


def filter_student_user_by_level(level):
    if level is None:
        return Q()
    return Q(student_user__grade__level=level)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSuperUser])
def get_all_users(request):
    params = request.query_params
    queryset = User.objects.filter(
        search_users_by_name(params.get('search'))
        & search_users_by_organization(params.get('organization'))
        & filter_student_user_by_grade(params.get('grade'))
        & filter_student_user_by_level(params.get('level'))
    ).order_by('-id')
    return get_paginated_response(queryset=queryset, request=request, serializer=UserSerializer)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_user_active_status(request, pk):
    user = User.objects.filter(id=pk).first()
    if user is None:
        return err_w_msg('User not found')

    user.is_active = not user.is_active
    user.save()

    return success_w_data(UserSerializer(user).data, 'User status updated successfully')


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    data = request.data

    username = data.get('username')

    if username is None:
        return err_w_msg('Username is required')

    user = User.objects.filter(username=username).first()
    if user is None:
        return err_w_msg('User not found')

    reset_code = generate()
    user.reset_code = reset_code
    user.save()

    # todo: update email template
    send_email(to=user.email, subject='School Management System Password Reset', body_params={
        'registration_url': f'https://askante.net/reset-password?code={reset_code}'
    })

    return success_w_msg('Reset link sent to your email')


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    data = request.data

    reset_code = data.get('reset_code')
    password = data.get('password')

    if reset_code is None or password is None:
        return err_w_msg('Reset code and password are required')

    user = User.objects.filter(reset_code=reset_code).first()
    if user is None:
        return err_w_msg('Invalid reset code')

    user.set_password(password)
    user.reset_code = None
    user.save()

    return success_w_msg('Password reset successfully')
