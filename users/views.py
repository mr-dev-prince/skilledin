from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from .models import CustomUser
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import UserSerializer, RegisterSerializer, ProfileUpdateSerializer, UserListSerializer, UserDetailSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=400)

class ProfileView(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ProfileUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tech_stack', 'location']  # exact match filters

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(username__icontains=search)
        return queryset
    
class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'uuid'