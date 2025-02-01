from rest_framework import serializers
from products.models import Review, Product, ProductTag,FavoriteProduct

class ProductSerializer(serializers.Serializer):
    name=serializers.CharField()
    description=serializers.CharField()
    price=serializers.FloatField()
    currency=serializers.ChoiceField(choices=['GEL', 'USD', 'EURO'])
    
class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class ReviewSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    content = serializers.CharField()
    rating = serializers.IntegerField()
    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    def create(self, validated_data):
        product = Product.objects.get(id=validated_data['product_id'])
        user = self.context['request'].user
        review = Review.objects.create(
            product=product,
            user=user,
            content=validated_data['content'],
            rating=validated_data['rating'],
        )
        return review
    
class ProductTagSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    tag_name = serializers.CharField()

    class Meta:
        model = ProductTag
        fields = ['id', 'product_id', 'tag_name']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data['product_id'])
        tag = ProductTag.objects.get_or_create(product=product, tag_name=validated_data['tag_name'])
        return tag
    
class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProduct
        fields = ['id', 'user', 'product']
    
    def validate(self, data):
        if 'user' not in data or 'product' not in data:
            raise serializers.ValidationError("Both user and product are required.")
        return data
