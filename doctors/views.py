from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Avg

from .models import DoctorProfile
from .serializers import DoctorSerializer


class DoctorViewSet(ReadOnlyModelViewSet):

    serializer_class = DoctorSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    search_fields = [
        'user__username',
        'speciality'
    ]

    ordering_fields = [
        'experience_years',
        'consultation_fee',
        "average_rating",
    ]

    filterset_fields = [
        'is_verified',
        'specialities'
    ]


    def get_queryset(self):

        return DoctorProfile.objects.filter(is_verified=True).select_related('user').prefetch_related('specialities', 'availability').annotate(average_rating=Avg('reviews__rating'))