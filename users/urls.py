from django.urls import path,  include
from users.views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('register', RegisterView, basename='register')

urlpatterns = [
    path('', include(router.urls)), 
]