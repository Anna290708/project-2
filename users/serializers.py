from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .models import *
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name')

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2=serializers.CharField(write_only=True, required=True)

    class Meta:
        model=User
        fields=('email', 'username', 'phone_number', 'password', 'password2', 'first_name', 'last_name')

    def validate(self,attrs):
        if attrs['password']!=attrs['password2']:
            raise serializers.ValidationError({'password': 'passwords dont match'})
        return attrs
    def create(self,validated_data):
        validated_data.pop('password2')
        user=User.objects.create_user(**validated_data)
        user.is_active=False
        user.save()
        return user
        
        
class PasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField()

    def validate_email(self,value):
        try:
            user=User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('მომხმარებელი არ მოიძებნა')
        return value
    

class passwordResetConfirmSerializer(serializers.Serializer):
    uidb64=serializers.CharField()
    token=serializers.CharField()
    password=serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2=serializers.CharField(write_only=True, required=True)

    def validate(Self,attrs):
        if attrs['password']!= attrs['password2']:
            raise serializers.ValidationError({'password':'parolebi ar emtxveva'})
        
        try:
            uid=force_str(urlsafe_base64_decode(attrs['uidb64']))
            user=User.objects.get(pk=uid)
        except(User.DoesNotExist, ValueError, TypeError, KeyError):
            raise serializers.ValidationError({'message':' momxmarebeli ver moidzebna'})
        
        token=attrs['token']
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({'message':"araswori an vadagasuli tokeni"})
        attrs['user']=user
        return attrs
    def save(self):
        user=self.validated_data['user']
        user.set_password(self.validated_data['password'])
        user.save()


class EmailCodeResendSerializer(serializers.Serializer):
    email=serializers.EmailField()

    def validate(self, attrs):
        email=attrs['email']
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'message': 'მომხმარებელი მსგავსი email-ით ვერ მოიძებნა'})
        
        if user.is_active:
            raise serializers.ValidationError({'message': 'მომხმარებელი უკვე გააქტიურებულია'})
        attrs['user']=user
        return attrs


class EmailCodeConfirmSerializer(serializers.Serializer):
    email=serializers.EmailField()
    code= serializers.CharField()

    def validate(self, attrs):
        email= attrs.get('email')
        code=attrs.get('code')

        try:
            user=User.objects.get(email=email)
            verification=EmailVerificationCode.objects.filter(user=user).first() 

            if not verification.code== code:
                raise serializers.ValidationError({"message": "კოდი არასწორია"}) 
            if verification.is_expired():
                raise serializers.ValidationError({'message': 'კოდი ვადაგასულია'})
        except(User.DoesNotExist, EmailVerificationCode.DoesNotExist):
            raise serializers.ValidationError({'message': 'მომხმარებელი ან მასთან დაკავშირებული კოდი ვერ მოიძებნა'})
        
        attrs['user']=user
        return attrs

        