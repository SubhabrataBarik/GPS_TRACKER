from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Child


# =========================================================
# CHILD INLINE
# =========================================================

class ChildInline(admin.TabularInline):

    model = Child

    extra = 0

    fields = (
        "name",
        "school_name",
        "grade",
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    show_change_link = True


# =========================================================
# USER ADMIN
# =========================================================

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    ordering = (
        "-created_at",
    )

    list_display = (
        "id",
        "full_name",
        "phone",
        "email",
        "is_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_login",
    )

    fieldsets = (

        (
            "Authentication",
            {
                "fields": (
                    "phone",
                    "password",
                )
            }
        ),

        (
            "Personal Information",
            {
                "fields": (
                    "full_name",
                    "email",
                )
            }
        ),

        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                )
            }
        ),

        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                )
            }
        ),
    )

    add_fieldsets = (

        (
            None,
            {
                "classes": (
                    "wide",
                ),

                "fields": (
                    "phone",
                    "full_name",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    inlines = [
        ChildInline,
    ]


# =========================================================
# CHILD ADMIN
# =========================================================

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):

    ordering = (
        "name",
    )

    list_display = (
        "id",
        "name",
        "parent",
        "school_name",
        "grade",
        "is_active",
        "created_at",
    )

    list_filter = (
        "grade",
        "school_name",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "school_name",
        "parent__full_name",
        "parent__phone",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "parent",
    )

    fieldsets = (

        (
            "Child Information",
            {
                "fields": (
                    "parent",
                    "name",
                    "school_name",
                    "grade",
                    "photo",
                )
            }
        ),

        (
            "Emergency Contact",
            {
                "fields": (
                    "emergency_contact_name",
                    "emergency_contact_phone",
                )
            }
        ),

        (
            "Status",
            {
                "fields": (
                    "is_active",
                )
            }
        ),

        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),
    )