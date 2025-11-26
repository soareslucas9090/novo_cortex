"""
Admin para o app Users
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 0
    fields = ('type', 'bio', 'avatar', 'status')
    can_delete = True


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'name',
        'is_active',
        'is_staff',
        'email_verified',
        'status',
        'date_joined'
    )
    
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'email_verified',
        'status',
        'date_joined'
    )
    
    search_fields = (
        'email',
        'name'
    )
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': (
                'phone',
                'birth_date',
                'email_verified',
                'status'
            )
        }),
    )
    
    ordering = ['email']
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': (
                'email',
                'phone',
                'birth_date',
                'email_verified',
                'status'
            )
        }),
    )
    
    inlines = [ProfileInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'type',
        'status',
        'created_at'
    )
    
    list_filter = (
        'type',
        'status',
        'created_at'
    )
    
    search_fields = (
        'user__email',
        'name'
    )
    
    fieldsets = (
        ('Informações Principais', {
            'fields': (
                'user',
                'type',
                'status'
            )
        }),
        ('Informações Adicionais', {
            'fields': (
                'bio',
                'avatar'
            )
        }),
    )
