from django.contrib import admin
from ..models import (
    User,
    ServiceProviderProfile,
    ProviderRequest,
    UserRoleChangeLog,
    ServiceCategory,
    Service,
    ServiceImage,
    ServiceContract,
)
from .user_admin import CustomUserAdmin
from .provider_admin import ServiceProviderProfileAdmin, ProviderRequestAdmin
from .log_admin import UserRoleChangeLogAdmin

# Registro de modelos en el panel de administración
admin.site.register(User, CustomUserAdmin)
admin.site.register(ServiceProviderProfile, ServiceProviderProfileAdmin)
admin.site.register(ProviderRequest, ProviderRequestAdmin)
admin.site.register(UserRoleChangeLog, UserRoleChangeLogAdmin)
admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(ServiceImage)
admin.site.register(ServiceContract)
