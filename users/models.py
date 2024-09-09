from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator, MinLengthValidator
from institutions.models.organization import Organization


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, username, role, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(username, role, first_name, last_name, password, **other_fields)

    def create_user(self, username, role, first_name, last_name, password, **other_fields):

        if not username:
            raise ValueError(_('Username must be provided'))

        user = self.model(username=username, role=role,
                          first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()

        return user


# creating user model
class User(AbstractBaseUser, PermissionsMixin):
    role_choices = (
        ('admin', 'admin'),
        ('employee', 'employee'),
        ('teacher', 'teacher'),
        ('student', 'student'),
        ('parent', 'parent'),
        ('publisher', 'publisher'),
    )

    gender_choices = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other'),
    )

    special_role_choices = (
        ('bursar', 'bursar'),
        ('librarian', 'librarian'),
    )

    username = models.CharField(
        _('username'),
        max_length=15,
        unique=True,
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(25),
        ],
        null=False,
        blank=False
    )
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    dp = models.URLField(null=True, blank=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True, related_name='org_users')

    last_session = models.DateTimeField(null=True, blank=True, default=None)

    role = models.CharField(
        max_length=15, choices=role_choices)
    is_organization_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_first_login = models.BooleanField(default=True)
    special_role = models.CharField(max_length=50, null=True, blank=True, choices=special_role_choices)
    reset_code = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    is_superuser = models.BooleanField(default=False)
    publisher = models.IntegerField(null=True, blank=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.username} - {self.role}'
