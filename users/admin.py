from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .models import User


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('username', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        })
    )

    list_display = ('id', 'username', 'email', 'is_staff')
    search_fields = ('username__exact',)
    ordering = ('id',)


admin.site.unregister(Group)
admin.site.register(User, MyUserAdmin)
