from django.db import models
from config.model_utils.models import TimeStampModel

class Category(TimeStampModel):
    name=models.CharField(max_length=255, unique=True)
    products=models.ManyToManyField('products.Product', related_name='categories')

class CategoryImage(TimeStampModel):
    category=models.ForeignKey('categories.Category', related_name='images', on_delete=models.CASCADE)

    active=models.BooleanField(default=False)
    image=models.ImageField(upload_to='categories/')