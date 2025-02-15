from rest_framework import serializers 
from products.models import *

 

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
        fields = ['product_id', 'content', 'rating']

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
        return Review.objects.create(product=product, user=user, **validated_data)



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


class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        source='products',
        queryset=Product.objects.all(),
        many=True, 
        write_only=True
    )

    class Meta:
        model = Cart
        fields = ['user', 'product_ids', 'products']

    def create(self, validated_data):
        user = validated_data.get('user')
        products = validated_data.pop('products')

        cart, _ = Cart.objects.get_or_create(user=user)
        cart.products.add(*products) 

        return cart
    
class ProductTagSerializer(serializers.ModelSerializer): 

    product_id = serializers.IntegerField(write_only=True) 

    tag_name = serializers.CharField() 
    class Meta: 

        model = ProductTag 

        fields = ['id', 'product_id', 'tag_name'] 

    def validate_product_id(self, value): 

        #produqtis arsebobis shemowmeba aucilebelia, rata ar davamatot tags ararsebul produqtze 

        if not Product.objects.filter(id=value).exists(): 

            raise serializers.ValidationError("Invalid product_id. Product does not exist.") 

        return value 
    def validate_tag_name(self, value): 

        #tag-is saxeli ar sheidzleba iyos carieli da unda iyso maqsimum 50 simbolo 
        if not value.strip(): 
            raise serializers.ValidationError("Tag name cannot be empty.") 

        if len(value) > 50: 

            raise serializers.ValidationError("Tag name is too long. Maximum 50 characters allowed.") 

        return value 
    def create(self, validated_data): 

        product = Product.objects.get(id=validated_data['product_id']) 

        tag, created = ProductTag.objects.get_or_create(product=product, tag_name=validated_data['tag_name']) 

        return tag 