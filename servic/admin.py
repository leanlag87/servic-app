from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ServiceProviderProfile, ProviderRequest, UserRoleChangeLog


# Configuración personalizada para el modelo User
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "user_type",
        "is_staff",
        "is_active",
    )
    list_filter = ("user_type", "is_staff", "is_active")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información Personal", {"fields": ("first_name", "last_name")}),
        (
            "Permisos",
            {
                "fields": (
                    "user_type",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Fechas Importantes", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "user_type"),
            },
        ),
    )


# Configuración para el perfil de prestador
class ServiceProviderProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "identification_type",
        "identification_number",
        "phone_number",
        "is_verified",
        "created_at",
    )
    list_filter = ("is_verified", "identification_type", "created_at")
    search_fields = ("user__email", "identification_number", "phone_number")
    readonly_fields = ("created_at", "updated_at")


# Configuración para las solicitudes de prestador
class ProviderRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "created_at", "updated_at", "reviewed_by")
    list_filter = ("status", "created_at")
    search_fields = ("user__email", "request_reason", "admin_response")
    readonly_fields = ("created_at", "updated_at")


# Configuración para el registro de cambios de rol
class UserRoleChangeLogAdmin(admin.ModelAdmin):
    list_display = ("user", "previous_role", "new_role", "changed_by", "changed_at")
    list_filter = ("previous_role", "new_role", "changed_at")
    search_fields = ("user__email", "reason")
    readonly_fields = ("changed_at",)


# Registro de modelos
admin.site.register(User, CustomUserAdmin)
admin.site.register(ServiceProviderProfile, ServiceProviderProfileAdmin)
admin.site.register(ProviderRequest, ProviderRequestAdmin)
admin.site.register(UserRoleChangeLog, UserRoleChangeLogAdmin)
