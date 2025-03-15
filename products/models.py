from django.db import models
from config.model_utils.models import TimeStampModel
from products.choices import Currency
from django.core.validators import MaxValueValidator
from users.models import *
class ProductTag(TimeStampModel):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Product(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', default=1)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=255, choices=Currency.choices, default=Currency.GEL)
    quantity = models.PositiveIntegerField()
    tags = models.ManyToManyField(ProductTag, related_name='products', blank=True)

    def __str__(self):
        return self.name

class Review(TimeStampModel):
    user=models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True,blank=True, related_name='reviews')
    product=models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    content=models.TextField()
    rating=models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    class Meta:
       unique_together=['product', 'user']

  
class Cart(TimeStampModel):
    products=models.ManyToManyField('products.Product', related_name='carts')
    user=models.OneToOneField('users.User' ,related_name='cart', on_delete=models.CASCADE)

class FavoriteProduct(TimeStampModel):
    product=models.ForeignKey('products.Product', related_name='favourite_products', on_delete=models.CASCADE)
    
    user=models.ForeignKey('users.User', related_name='favourite_product' , on_delete=models.SET_NULL, null=True , blank=True)

class ProductImage(TimeStampModel):
    image=models.ImageField(upload_to='products/')
    product=models.ForeignKey('products.Product',related_name='images', on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField(default=1)
    price_at_time_of_additions=models.FloatField()


    def __str__(self):
        return f'{self.product.name} - {self.quantity}' 


    def get_total_price(self):
        return self.quantity * self.price_at_time_of_additions
    
    


