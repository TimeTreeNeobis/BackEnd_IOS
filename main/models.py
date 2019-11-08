import jwt

from datetime import datetime, timedelta

from django.conf import settings

from .managers import UserManager
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, Group
)


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Choice(models.Model):
    choice = models.CharField(max_length=500)

    def __str__(self):
        return self.choice


class Poll(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question = models.TextField()

    def __str__(self):
        return self.question


class Event(models.Model):
    group = models.ManyToManyField(Group)
    title = models.CharField(max_length=255)
    info_text = models.TextField()
    day = models.DateField()
    place = models.CharField(max_length=255)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=255)
    site_link = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=255)
    name_short = models.CharField(max_length=255)
    site_link = models.CharField(max_length=255)

    def __str__(self):
        return self.name_short


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(db_index=True, max_length=255, null=True)
    surname = models.CharField(db_index=True, max_length=255, null=True)
    login = models.CharField(max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)

    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    groups = models.ManyToManyField(Group, related_name='departament')

    university = models.ForeignKey(University, null=True, default=None, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, null=True, default=None, on_delete=models.SET_NULL)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    def __str__(self):
        return self.login

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.name + self.surname

    def get_short_name(self):
        return self.login

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Contact(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    choices = [
        (1, 'Phone'),
        (2, 'Address'),
        (3, 'Facebook'),
        (4, 'Telegram')
    ]

    type = models.IntegerField(choices=choices, default=1)

    value = models.CharField(max_length=1000)

    def __str__(self):
        return self.value
