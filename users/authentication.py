import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from users.models import User
from core.settings import SECRET_KEY


class CSRFCheck(CsrfViewMiddleware):
    def __reject(self, request, reason):
        return reason


class CustomJwtAuth(BaseAuthentication):
    '''
        custom authentication class for DRF and JWT
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    '''

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            # header = 'Token(0) xxxxxxxxxxxxxxxxxxxxxxxx(1)'
            access_token = auth_header.split(' ')[1]
            payload = jwt.decode(
                access_token, SECRET_KEY, algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Invalid Credentials')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid Credentials')

        # querying the user
        user = User.objects.filter(id=payload['id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User account not activated')

        # self.enforce_csrf(request)
        return (user, None)

    # def enforce_csrf(self, request):
    #     """
    #     Enforce CSRF validation
    #     """
    #
    #     check = CSRFCheck()
    #     # populates request.META['CSRF_COOKIE'], which is used in process_view()
    #     check.process_request(request)
    #     reason = check.process_view(request, None, (), {})
    #     if reason:
    #         # CSRF failed, bail with explicit error message
    #         raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
