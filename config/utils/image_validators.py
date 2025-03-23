from django.core.validators import ValidationError
from PIL import Image
from django.apps import apps
def validate_image_size(image):
    size=image.size
    limit=5
    if size > limit*1024*1024 :
        raise ValidationError(f'ფაილი არ უნდა აღემატებოდეს {limit}MB')

def validate_image_resolution(image):
    image=Image.open(image)
    width,height= image.size
    minimum_width, minimum_height= 300,300
    maximum_width, maximum_height=4000,4000
    if width>= maximum_width or height>= maximum_height:
        raise ValidationError('სურათის გაფართოება არ უნდა აღემატებოდეს 4000x4000 პიქსელს')
    if width<= minimum_width or height<= minimum_height:
        raise ValidationError('სურათის გაფართოება უნდა იყოს 300x300 პიქსელზე ნაკლები')
   
def validate_image_count(product_id):
    ProductImage=apps.get_model('products', 'ProductImage')
    limit=5
    count=ProductImage.objects.filter(product_id=product_id).count()
    if count>=limit:
        raise ValidationError(f'ერთ პროდუქტზე, მაქსიმუმ შეგვიძლია {limit} სურათის შენახვა')
