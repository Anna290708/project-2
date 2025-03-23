from django.db import models
from config.model_utils.models import TimeStampModel
from config.utils.image_validators import *

class Category(TimeStampModel):
    name=models.CharField(max_length=255, unique=True)
    products=models.ManyToManyField('products.Product', related_name='categories')

    def __str__(self):
        return self.name
class CategoryImage(TimeStampModel):
    category=models.ForeignKey('categories.Category', related_name='images', on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)
    image=models.ImageField(upload_to='categories/',validators=[validate_image_size, validate_image_resolution])