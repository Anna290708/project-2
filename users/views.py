from django.shortcuts import render
from rest_framework.mixins import *
from rest_framework.viewsets import GenericViewSet
from users.models import *
from users.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets,status, response
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from users.permissions import IsOwnerOrReadOnly  
# from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view
# from django.core.validators import ValidationError
import random
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset=User.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=UserSerializer

class RegisterView(CreateModelMixin, GenericViewSet):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer

    def create(self,request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            self.send_verification_code(user)
            return Response({'detail': 'User registered successfully.Verification code sent to email'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_verification_code(self, user):
        code=str(random.randint(100000, 999999))
        
        EmailVerificationCode.objects.update_or_create(
            user=user,
            defaults={'code': code, 'created_at': timezone.now()}
        )
        subject='Your verification code'
        message=f'Hello {user.username}, your verification code is {code} '
        send_mail(subject, message, 'no-reply@example.com', [user.email])

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

class PasswordResetViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = PasswordResetSerializer
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = request.build_absolute_uri(
                 reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
)
            
            
            send_mail(
                'პაროლის აღდგენა',
                f'დააჭირეთ ლინკს რეგისტრაციისთვის {reset_url}',
                'example@gmail.com',
                [user.email],
                fail_silently = False
            )
            
            return Response({'message': 'გაიგზავნა'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordResetConfirmViewSet(CreateModelMixin,GenericViewSet):
    serializer_class=passwordResetConfirmSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('idb64', openapi.IN_PATH, description='User ID (Base64 encoded )', type=openapi.TYPE_STRING),
            openapi.Parameter('token', openapi.IN_PATH, description='Password reset token', type=openapi.TYPE_STRING),
        ]
        )
    def create(self,request,**kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'პაროლი წარმატებით არის შეცვლილი'}, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
