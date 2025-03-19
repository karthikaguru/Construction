from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser



class CustomUserAdmin(UserAdmin):
    # Display relevant fields in the admin form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Login details
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),  # Personal details
        ('Roles', {'fields': ('role', 'is_authorized')}),  # Role and authorization
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  # Permissions
    )

    # Fields for user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_authorized')}
         ),
    )

    # Fields displayed in the admin user list
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'role', 'is_authorized', 'is_staff', 'is_superuser'
    )

    # Filters for the admin user list
    list_filter = ('role', 'is_authorized', 'is_staff', 'is_superuser')

# Register the CustomUser model with the customized admin
admin.site.register(CustomUser, CustomUserAdmin)
