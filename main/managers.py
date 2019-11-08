from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, login, email, password, name=None, surname=None, role=None, phone=None, **extra_fields):
        if login is None:
            raise ValueError('Users must have a login.')

        if email is None:
            raise ValueError('Users must have a email.')

        email = self.normalize_email(email)

        user = self.model(
            role=role,
            login=login,
            name=name,
            surname=surname,
            email=email,
            phone=phone,
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, login, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is None:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is None:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(login, email, password, **extra_fields)