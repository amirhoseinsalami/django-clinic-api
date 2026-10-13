from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (

        (

            'Role',

            {'fields' : ("role",)}

        ),
    
    )

# because Django already has a User admin interface.
# We extended it and added role