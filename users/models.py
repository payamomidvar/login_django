import random

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManger(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))

        user = self.model(username=username,
                          email=email,
                          is_active=True,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        username = email.split('@', 1)[0]

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=32,
                                help_text=_(
                                    'Required. 30 characters or fewer starting with a letter.'
                                    ' Letters, digits and underscore only.'),
                                validators=[
                                    validators.RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
                                                              _('Enter a valid username starting with a-z. '
                                                                'This value may contain only letters, numbers '
                                                                'and underscore characters.'),
                                                              'invalid'),
                                ],
                                )
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('Staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.')
                                   )
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'
    ))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(_('last seen date'), null=True)

    objects = UserManger()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
