from rest_framework import serializers 
from products.models import *

     
class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductTag
        fields=['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField() 
    description = serializers.CharField() 
    price = serializers.FloatField() 
    currency = serializers.ChoiceField(choices=['GEL', 'USD', 'EURO']) 
    quantity = serializers.IntegerField()
    class Meta:
        model = Product  # Specify the model
        fields = ['name', 'description', 'price', 'currency', 'quantity'] 


class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_id', 'product_id', 'content', 'rating']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data.pop('product_id'))
        user = self.context['request'].user
        existing_reviews=Review.objects.filter(product=product , user=user)
        if existing_reviews.exists():
            raise serializers.ValidationError('you already reviewed this product')
            
        return Review.objects.create(product=product, user=user, **validated_data)

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField() 
    description = serializers.CharField() 
    price = serializers.FloatField() 
    currency = serializers.ChoiceField(choices=['GEL', 'USD', 'EURO']) 
    quantity = serializers.IntegerField()
   
    reviews = ReviewSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        source="tags",
        queryset=ProductTag.objects.all(),
        many=True,
        write_only=True
    )
    tags = ProductTagSerializer(many=True, read_only=True)
    class Meta:
        model = Product  
        fields = ['name', 'description', 'price', 'currency', 'quantity', 'tag_ids', 'tags','reviews'] 

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        product = Product.objects.create(**validated_data)
        product.tags.set(tags)
        return product

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags.set(tags) 
        return super().update(instance, validated_data)
                              

class FavoriteProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = FavoriteProduct
        fields = ['id', 'user', 'product_id', 'product']
        read_only_fields = ['id', 'product']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        user = validated_data.pop('user')
        
        product = Product.objects.get(id=product_id)
        favorite, created = FavoriteProduct.objects.get_or_create(user=user, product=product)

        if not created:
            raise serializers.ValidationError("This product is already in favorites.")

        return favorite

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Nested product details (read-only)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price_at_time_of_additions', 'total_price']
        read_only_fields = ['price_at_time_of_additions']

    def get_total_price(self, obj):
        return obj.get_total_price()

    def create(self, validated_data):
        # Extract product_id from the validated data
        product = validated_data.pop('product_id')  # Get the product instance from the product_id
        
        # Ensure the cart is created or fetched for the current user
        user = self.context['request'].user
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Create the CartItem and set product as a ForeignKey instance, not just the id
        cart_item = CartItem.objects.create(
            cart=cart,  # Set the cart reference
            product=product,  # Set the actual product instance, not the product_id
            quantity=validated_data.get('quantity', 1),  # Default to 1 if quantity is not provided
            price_at_time_of_additions=product.price  # Use the product's price at the time of addition
        )
        return cart_item



    
class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['user', 'items', 'total']

    def get_total(self, obj):
        return sum(item.get_total_price() for item in obj.items.all()) 
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['id', 'image', 'product']