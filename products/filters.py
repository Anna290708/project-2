from django_filters import FilterSet, NumberFilter
from products.models import Product, Review

class ProductFilter(FilterSet):
    price_min=NumberFilter(field_name='price', lookup_expr='gte')
    price_max= NumberFilter(field_name='price', lookup_expr='lte')

    class meta:
        model=Product
        fields= ['categories', 'price_min' , 'price_max']

class ProductReview(FilterSet):
    review_min=NumberFilter('rating', lookup_expr='gte')
    review_max=NumberFilter('rating', lookup_expr='lte')

    class meta:
        model=Review
        fields= ['review_min', 'review_max']

