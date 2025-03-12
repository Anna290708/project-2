from django.shortcuts import render
from rest_framework.mixins import *
from rest_framework.viewsets import GenericViewSet
from users.models import User
from users.serializers import *
from rest_framework.permissions import IsAuthenticated

class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset=User.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=UserSerializer

class RegisterView(CreateModelMixin, GenericViewSet):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
