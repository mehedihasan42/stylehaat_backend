from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.tokens import RefreshToken

class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "User registered successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    