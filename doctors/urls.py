from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import DoctorViewSet, SpecialityListView


router = DefaultRouter()

router.register(
    'doctors', # endpoint
    DoctorViewSet,
    basename='doctor'
)

urlpatterns = [
    path(
        "specialities/",
        SpecialityListView.as_view(),
        name="speciality-list",
    ),
    path('', include(router.urls))
]
