from .auth_views import RegisterView, CustomTokenObtainPairView
from .user_views import UserProfileView, UserRoleChangeView
from .provider_views import (
    ServiceProviderProfileView,
    ProviderRequestView,
    ProviderRequestListView,
    ProviderRequestDetailView,
)
from .service_views import (
    ServiceCategoryListView,
    ServiceCategoryDetailView,
    ServiceCreateView,
    ServiceListView,
    ServiceDetailView,
    ServiceImageUploadView,
    ServiceImageDeleteView,
    ServiceImageSetPrimaryView,
)


__all__ = [
    "RegisterView",
    "CustomTokenObtainPairView",
    "UserProfileView",
    "UserRoleChangeView",
    "ServiceProviderProfileView",
    "ProviderRequestView",
    "ProviderRequestListView",
    "ProviderRequestDetailView",
    "ServiceCategoryListView",
    "ServiceCategoryDetailView",
    "ServiceCreateView",
    "ServiceListView",
    "ServiceDetailView",
    "ServiceImageUploadView",
    "ServiceImageDeleteView",
    "ServiceImageSetPrimaryView",
]
