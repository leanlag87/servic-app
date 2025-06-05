from django.urls import path
from ..views import (
    ServiceCategoryListView,
    ServiceCategoryDetailView,
    ServiceCreateView,
    ServiceListView,
    ServiceDetailView,
    ServiceImageUploadView,
    ServiceImageDeleteView,
    ServiceImageSetPrimaryView,
)

urlpatterns = [
    # URLs para categorías de servicios
    path(
        "categories/", ServiceCategoryListView.as_view(), name="service-category-list"
    ),
    path(
        "categories/<int:pk>/",
        ServiceCategoryDetailView.as_view(),
        name="service-category-detail",
    ),
    # URLs para servicios
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("services/create/", ServiceCreateView.as_view(), name="service-create"),
    path("services/<int:pk>/", ServiceDetailView.as_view(), name="service-detail"),
    # URLs para imágenes de servicios
    path(
        "services/<int:service_id>/images/",
        ServiceImageUploadView.as_view(),
        name="service-image-upload",
    ),
    path(
        "services/images/<int:pk>/",
        ServiceImageDeleteView.as_view(),
        name="service-image-delete",
    ),
    path(
        "services/images/<int:pk>/set-primary/",
        ServiceImageSetPrimaryView.as_view(),
        name="service-image-set-primary",
    ),
]
