#==>Library Import
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
#==>Local Import
from .forms import UserChangeForm, UserCreationForm
from .models import User, OtpCode, Profile


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'phone', 'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'email_activate')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email', 'username')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(OtpCode)
admin.site.register(Profile)
admin.site.unregister(Group)