from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django.db.models import Avg

from .models import DoctorProfile, Speciality
from .serializers import DoctorSerializer, SpecialitySerializer

from django.core.cache import cache
from rest_framework.generics import ListAPIView
from rest_framework.response import Response


@method_decorator(cache_page(300), name="list")
class DoctorViewSet(ReadOnlyModelViewSet):

    serializer_class = DoctorSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    search_fields = [
        "user__username",
        "specialities__name",
    ]

    ordering_fields = [
        "experienced_years",
        "consultation_fee",
        "average_rating",
    ]

    filterset_fields = [
        'is_verified',
        'specialities'
    ]


    def get_queryset(self):

        return DoctorProfile.objects.filter(is_verified=True).select_related('user').prefetch_related('specialities', 'availability').annotate(average_rating=Avg('reviews__rating'))




class SpecialityListView(ListAPIView):
    serializer_class = SpecialitySerializer

    def list(self, request, *args, **kwargs):
        cache_key = "clinic:specialities:v1"

        data = cache.get(cache_key)

        if data is None:
            data = list(
                Speciality.objects
                .order_by("name")
                .values("id", "name")
            )

            cache.set(
                cache_key,
                data,
                timeout=300,
            )

        page = self.paginate_queryset(data)

        if page is not None:
            return self.get_paginated_response(page)

        return Response(data)
