from django.shortcuts import render 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from products.models import * 
from rest_framework import status 
from products.serializers import * 
from django.shortcuts import get_object_or_404 
from rest_framework.views import APIView 
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
 



@api_view(['GET', 'POST']) 
def cart_view(request): 

    if request.method == 'GET': 

        cart_items = Cart.objects.all() 

        if not cart_items.exists():  

            return Response({'cart': []})   
        serializer = CartSerializer(cart_items, many=True) 

        return Response({'cart': serializer.data}) 

    elif request.method == 'POST': 

        serializer = CartSerializer(data=request.data) 

        if serializer.is_valid(): 

            product_id = serializer.validated_data['product_id'] 

            quantity = serializer.validated_data['quantity'] 
            product = Product.objects.get(id=product_id) 
            cart_item, created = Cart.objects.get_or_create(product=product, defaults={'quantity': quantity}) 

            if not created: 

                cart_item.quantity += quantity 

                cart_item.save() 

             

            return Response({'message': 'Product added to cart'}, status=status.HTTP_201_CREATED) 

         

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

     

@api_view(['GET', 'POST']) 

def product_tag_view(request, product_id): 

    product = get_object_or_404(Product, id=product_id) 
    if request.method == 'GET': 

        tags = ProductTag.objects.filter(product=product) 

        serializer = ProductTagSerializer(tags, many=True) 

        return Response({'tags': serializer.data})

    elif request.method == 'POST': 

        serializer = ProductTagSerializer(data=request.data) 

        if serializer.is_valid(): 

            tag_name = serializer.validated_data['tag_name'] 

            if ProductTag.objects.filter(product=product, tag_name=tag_name).exists(): 

                return Response({'error': 'Tag already exists for this product'}, status=status.HTTP_400_BAD_REQUEST) 

            ProductTag.objects.create(product=product, tag_name=tag_name) 
            return Response({'message': 'Tag added successfully'}, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

 

@api_view(['GET', 'POST']) 

def favorite_product_view(request, user_id): 
    if request.method == 'GET': 
        favorites = FavoriteProduct.objects.filter(user_id=user_id) 
        serializer = FavoriteProductSerializer(favorites, many=True) 
        return Response({'favorites': serializer.data}) 

    elif request.method == 'POST': 
        serializer = FavoriteProductSerializer(data=request.data) 
        if serializer.is_valid(): 
            product_id = serializer.validated_data['product_id'] 
            product = get_object_or_404(Product, id=product_id) 
            if FavoriteProduct.objects.filter(user_id=user_id, product=product).exists(): 
                return Response({'error': 'Product is already in favorites'}, status=status.HTTP_400_BAD_REQUEST) 
            FavoriteProduct.objects.create(user_id=user_id, product=product) 
            return Response({'message': 'Product added to favorites successfully'}, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

 