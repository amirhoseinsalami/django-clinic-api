from rest_framework.permissions import IsAuthenticated
from rest_framework.views import ModelViewSet

from .models import Review
from .services import create_review
from .serializers import ReviewSerializer


class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Review.objects.select_related(
            'patient',
            'doctor',
            'doctor__user'
        )

    
    def perform_crate(self, serializer):

        review = create_review(
            patient=self.request.user,

            appointment = serializer.validated_data['appointment'],

            rating = serializer.validated_data['rating'],

            comment = serializer.validated_data.get('comment', '')
        )


        serializer.instance = review

        