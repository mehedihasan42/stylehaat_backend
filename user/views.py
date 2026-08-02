from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializer import *
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer  
    # permission_classes = [IsAdminUser] 

    def get_queryset(self):
        queryset = User.objects.all()

        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)

        return queryset


class UserByUserNameView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field = 'username'


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


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)    
    
    def put(self,request):
        serializer = UserSerializer(
            request.user,
            data = request.data,
            partial = True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)   
        
        return Response(serializer.errors,status=400)    