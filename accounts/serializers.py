from rest_framework import serializers
from .models import User, PatientProfile

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'username', 
            'email',
            'password'
        ]

    def create(self, validated_data):  # when serializer.save(), create runs

        user = User.objects.create_user(
            **validated_data,
            role=User.Role.PATIENT
        )

        PatientProfile.objects.create(
            user=user
        )

        return user


class PatientProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientProfile

        fields = [
            'phone',
            'birth_date'
        ]


class MeSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField() # automatically call get_profile

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'role',
            'profile'
        ]

    def get_profile(self, obj):

        if obj.role == User.Role.PATIENT:
            return PatientProfileSerializer(
                obj.patient_profile
            ).data

        if obj.role == User.Role.DOCTOR:
            from doctors.serializers import DoctorSerializer

            return DoctorSerializer(
                obj.doctor_profile
            ).data

        return None