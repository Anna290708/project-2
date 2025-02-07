from rest_framework import serializers
from products.models import Review, Product, ProductTag, FavoriteProduct

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    currency = serializers.ChoiceField(choices=['GEL', 'USD', 'EURO'])

    def validate_price(self, value):
        # produqtis fasi arunda iyos uaryofiti

        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value


class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

<<<<<<< HEAD
    def validate_product_id(self, value):
        #vamowmebt aris tuara bazashi es produqti
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value


class ReviewSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    content = serializers.CharField()
    rating = serializers.IntegerField()

    def validate_product_id(self, value):
        #produqtis arsebobis shemowmeba bazashi
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
=======
class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['product_id', 'content', 'rating']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
>>>>>>> 859a6da604bc5dfa33291e864af507a5aff7e930
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def validate_rating(self, value):
        #reitingi unda ios 1-dan 5mde,anu shefaseba igive
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data.pop('product_id'))
        user = self.context['request'].user
<<<<<<< HEAD
        #vqmnit axal mimoxilvas arsebuli momxmareblistvis da produqtistvis
        review = Review.objects.create(
            product=product,
            user=user,
            content=validated_data['content'],
            rating=validated_data['rating'],
        )
        return review


=======
        return Review.objects.create(product=product, user=user, **validated_data)
    
>>>>>>> 859a6da604bc5dfa33291e864af507a5aff7e930
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


class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProduct
        fields = ['id', 'user', 'product']
        read_only_fields = ['user'] #momxmareblis veli mxolod wasakitxia,radgan is sistemashi avtomaturad emateba 
    def validate(self, data):
        user = self.context['request'].user
        product = data.get('product')
        #vamowmebt aris tuara produqti ukve damatebuli favoritebshi aam momxmareblistvis
        if FavoriteProduct.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("This product is already in your favorites.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        favorite_product = FavoriteProduct.objects.create(user=user, **validated_data)
        return favorite_product
