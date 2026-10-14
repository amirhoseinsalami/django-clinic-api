from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, MeSerializer

from drf_spectacular.utils import extend_schema



class RegisterView(APIView):

    @extend_schema(request=RegisterSerializer, responses=RegisterSerializer)
    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    'message' : "User created successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class MeView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @extend_schema(responses=MeSerializer)
    def get(self, request):

        serializer = MeSerializer(request.user)

        return Response(serializer.data)

    