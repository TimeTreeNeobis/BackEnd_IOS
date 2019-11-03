from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.utils import timezone
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


class University(models.Model):
    name = models.CharField(max_length=255)
    name_short = models.CharField(max_length=255)
    site_link = models.CharField(max_length=255)


class User(AbstractBaseUser, PermissionsMixin):
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    name = models.CharField(db_index=True, max_length=255, null=True)
    surname = models.CharField(db_index=True, max_length=255, null=True)
    login = models.CharField(max_length=255, unique=True)
    groups = models.ManyToManyField(Group, related_name='departament')
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    university = models.ForeignKey(University, null=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    def __str__(self):
        return self.login

