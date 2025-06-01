from django.urls import path
from servic.views.auth_views import RegisterView, CustomTokenObtainPairView
from servic.views.user_views import UserProfileView, UserRoleChangeView
from servic.views.provider_views import (
    ServiceProviderProfileView,
    ProviderRequestView,
    ProviderRequestListView,
    ProviderRequestDetailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('provider/profile/', ServiceProviderProfileView.as_view(), name='provider-profile'),
    path('users/<int:user_id>/change-role/', UserRoleChangeView.as_view(), name='change-user-role'),
    
    # Nuevas URLs para solicitudes de prestador
    path('provider/request/', ProviderRequestView.as_view(), name='create-provider-request'),
    path('provider/requests/', ProviderRequestListView.as_view(), name='list-provider-requests'),
    path('provider/requests/<int:pk>/', ProviderRequestDetailView.as_view(), name='review-provider-request'),
] 

## Aqui definimos las rutas de la API similar al archivo "usersRoutes.js"
# Estas son las rutas que vamos a testear en insomnia