from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from categories.serializers import *
from categories.models import *
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class CategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends=[SearchFilter]
    search_fields=['name']


class CategoryImageViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = CategoryImage.objects.all()
    serializer_class = CategoryImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(category_id=self.kwargs['category_pk'])
