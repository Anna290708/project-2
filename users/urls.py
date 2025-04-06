from django.urls import path,  include
from users.views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('register', RegisterView, basename='register')
router.register('profile', ProfileViewSet, basename='profile')
router.register('password_reset', PasswordResetViewSet, basename='password_reset')
urlpatterns = [
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmViewSet.as_view({'post': 'create'}), name='password_reset_confirm'),
    path('', include(router.urls)),
]
