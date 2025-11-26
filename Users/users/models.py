from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager
from AppCore.core.helpers.helpers_mixin import ModelHelperMixin
from AppCore.core.business.business_mixin import ModelBusinessMixin

from .business import UserBusiness
from .helpers import UserHelpers
from . import choices


class UserManager(Base404ExceptionManager):
    def create_user(self, email, name, password=None, phone=None, birth_date=None, profiles=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um email')
        if not name:
            raise ValueError('O usuário deve ter um nome')
        
        email = self.normalize_email(email)
        
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('status', choices.USER_STATUS_ATIVO)
        
        user = self.model(
            email=email,
            name=name,
            phone=phone,
            birth_date=birth_date,
            **extra_fields
        )
        
        if password:
            user.set_password(password)
        
        user.save()
        
        return user
    
    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('status', choices.USER_STATUS_ATIVO)
        extra_fields.setdefault('email_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True')
        
        return self.create_user(
            email=email,
            name=name,
            password=password,
            **extra_fields
        )
    

class User(
    ModelHelperMixin, ModelBusinessMixin, AbstractBaseUser, PermissionsMixin, BasicModel
):
    name = models.CharField(
        'Nome',
        max_length=150,
    )
    email = models.EmailField('Email', unique=True)
    email_verified = models.BooleanField(
        'Email Verificado',
        default=False
    )
    phone = models.CharField(
        'Telefone',
        max_length=20,
        blank=True,
        null=True
    )
    birth_date = models.DateField(
        'Data de Nascimento',
        blank=True,
        null=True
    )
    status = models.IntegerField(
        'Status',
        choices=choices.USER_STATUS_CHOICES,
        default=choices.USER_STATUS_ATIVO
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True
    )
    is_staff = models.BooleanField(
        'Equipe',
        default=False
    )
    is_superuser = models.BooleanField(
        'Superusuário',
        default=False
    )
    date_joined = models.DateTimeField(
        'Data de Criação',
        default=timezone.now
    )

    objects = UserManager()
    USERNAME_FIELD = "email"
    
    helper_class = UserHelpers
    business_class = UserBusiness
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']

    def __str__(self):
        return self.name

    @property
    def account_business(self):
        from Users.account.business import AccountBusiness

        return AccountBusiness(object_instance=self)

    @property
    def account_helper(self):
        from Users.account.helpers import AccountHelper

        return AccountHelper(object_instance=self)


class PasswordResetCode(BasicModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_code',
        verbose_name='Usuário'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(null=False)
    code = models.IntegerField(null=False)
    validated = models.BooleanField(default=False)

    def __str__(self):
        return f"User {self.user}, code {self.code}"

    class Meta:
        db_table = 'password_reset_codes'
        verbose_name = 'Código de redefinição de senha'
        verbose_name_plural = 'Códigos de redefinição de senha'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=["user", "code"], name="unique_code_user_constraint"
            )
        ]


class Profile(BasicModel, ModelHelperMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='profiles',
        verbose_name='Usuário'
    )
    type = models.CharField(
        'Tipo',
        max_length=10,
        choices=choices.PROFILE_TYPE_CHOICES,
        default=choices.PROFILE_TYPE_USER
    )
    bio = models.TextField(
        'Biografia',
        blank=True,
        null=True
    )
    avatar = models.CharField(
        'Avatar',
        max_length=255,
        blank=True,
        null=True
    )
    status = models.IntegerField(
        'Status',
        choices=choices.PROFILE_STATUS_CHOICES,
        default=choices.PROFILE_STATUS_ATIVO
    )
    
    class Meta:
        db_table = 'profiles'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=["user", "type"], name="unique_profile_user_constraint"
            )
        ]
    
    def __str__(self):
        return f'{self.user.name} - {self.get_type_display()}'
