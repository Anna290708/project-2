from django.shortcuts import render 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from products.models import * 
from rest_framework import status 
from products.serializers import * 
from django.shortcuts import get_object_or_404 
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin,UpdateModelMixin, DestroyModelMixin


class ProductViewSet(ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView): 
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    def get(self,request,pk=None, *args, **kwargs): 
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request  , *args ,**kwargs)
    def post(self,request, *args, **kwargs): 
        return self.create(request,*args ,**kwargs )
    def put(self,request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def patch(self,request, *args, **kwargs):
        return self.partial_update(request,*args, **kwargs )
    def delete(self,request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReviewViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
    serializer_class=ReviewSerializer
    queryset=Review.objects.all()

    def get(self,request, *args, **kwargs):
        return self.list(request , *args ,**kwargs)
    def post(self,request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
 
class FavoriteProductViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class CartViewSet(ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
class TagList(ListModelMixin, GenericAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)