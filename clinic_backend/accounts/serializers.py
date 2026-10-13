from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True   # To not appear in serializer.data(Also the saved password in the DB is hashed)
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "role"
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            **validated_data
        )

        return user