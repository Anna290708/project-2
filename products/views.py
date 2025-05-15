from products.models import * 
from products.serializers import * 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import *
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin,UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from products.pagination import *
from products.filters import *
from rest_framework.exceptions import PermissionDenied
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from .permissions import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
class ProductViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,IsObjectOwnerOrReadOnly] 
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    pagination_class = ProductPagination
    throttle_classes = [AnonRateThrottle]
    
    @action(detail=False, methods=['GET'])
    def my_products(self, request,):
        products = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)



class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrReadOnly]
    filter_backends=[DjangoFilterBackend]
    filterset_class=ProductReview
    throttle_classes=[AnonRateThrottle]
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)



class FavoriteProductViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes=[ScopedRateThrottle]
    trottle_scope='likes'
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class CartViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class ProductTagViewSet(ListModelMixin, GenericViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]

class ProductImageViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes=[MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        try:
         return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response ({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs.get('product_pk'))
    
    
    
class CartItemViewSet(ModelViewSet):
    queryset=CartItem.objects.all()
    serializer_class=CartItemSerializer
    permission_classes=[IsAuthenticated, IsObjectOwnerOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)
    