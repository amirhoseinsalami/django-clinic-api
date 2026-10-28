from rest_framework import serializers
from .models import DoctorAvailability, DoctorProfile, Speciality

from accounts.models import User


class SpecialitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Speciality
        fields = [
            'id',
            'name'
        ]

class DoctorUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name'
        ]


class AvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorAvailability
        fields = [
            'id',
            'day_of_week',
            'start_time',
            'end_time'
        ]


class DoctorSerializer(serializers.ModelSerializer):

    user = DoctorUserSerializer(
        read_only=True
    )

    availability = AvailabilitySerializer(
        read_only=True,
        many = True
    )

    average_rating = serializers.FloatField(read_only=True)

    specialities = SpecialitySerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = DoctorProfile

        fields = [
            'id',
            'user',
            'specialities',
            'bio',
            'experienced_years',
            'consultation_fee',
            'availability',
            'average_rating'
        ]