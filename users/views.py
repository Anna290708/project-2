from django.shortcuts import render
from rest_framework.mixins import *
from rest_framework.viewsets import GenericViewSet
from users.models import User
from users.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsOwnerOrReadOnly  

class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset=User.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=UserSerializer

class RegisterView(CreateModelMixin, GenericViewSet):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer

class ProfileViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        allowed_fields = {"username", "email", "phone_number", "password"}
        update_data = {key: value for key, value in self.request.data.items() if key in allowed_fields}
        
        if "password" in update_data:
            update_data["password"] = make_password(update_data["password"])
        
        serializer.validated_data.update(update_data)
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
