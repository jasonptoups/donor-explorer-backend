from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions


from .serializers import SavedDonorSerializer
from .serializers import UserSerializer
from .serializers import NewUserSerializer
from .models import SavedDonor


class SavedDonorList(generics.ListCreateAPIView):
    queryset = SavedDonor.objects.all()
    serializer_class = SavedDonorSerializer


class SavedDonorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SavedDonor.objects.all()
    serializer_class = SavedDonorSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateAuth(generics.CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = NewUserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
