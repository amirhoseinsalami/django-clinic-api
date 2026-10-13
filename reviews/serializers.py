from rest_framework import serializers

from .models import Review

class ReviewSerializer(serializers.ModelSerializer):

    pateint_name = serializers.CharField(
        source_name='patient.username',
        read_only=True
    )

    doctor_name = serializers.CharField(
        source_name='doctor.user.username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'doctor_name',
            'patient_name',
            'rating',
            'comment',
            'created_at'
        ]

        read_only_fields = [
            'created_at'
        ]

    
    def validate_rating(self, value):
        if value > 5 or value < 1:
            raise serializers.ValidationError("Rating muse be between 1 and 5")
        
        return value