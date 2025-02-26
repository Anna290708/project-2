from django.urls import path, include
from categories.views import *
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)

categories_router = routers.NestedDefaultRouter(router, 'categories', lookup='category')
categories_router.register('images', CategoryImageViewSet, basename='category-images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(categories_router.urls)),
]