
from products.models import * 
from products.serializers import * 
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import *
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin,UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet

class ProductViewSet(ModelViewSet): 
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(ListCreateAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_id'])


class FavoriteProductViewSet(ModelViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]
    http_method_names=['get', 'post' ,'delete']
    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
    
    
class CartViewSet(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    
    
class ProductTagListView(ListAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]

class ProductImageViewSet(ModelViewSet):
    queryset=ProductImage.objects.all()
    serializer_class=ProductImageSerializer
    permission_classes=[IsAuthenticated]
    http_method_names=['get', 'post' ,'delete']
    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs.get('product_id'))
 