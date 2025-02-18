from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from categories.serializers import *
from categories.models import *
from rest_framework.permissions import IsAuthenticated
class CategoryListView(ListModelMixin, GenericAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes= [IsAuthenticated]
    def get(self,request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class CategoryDetailView(RetrieveModelMixin, GenericAPIView):
    queryset=Category.objects.all()
    serializer_class=CategoryDetailSerializer
    permission_classes= [IsAuthenticated]
    def get(self,request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
class CategoryImageViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = CategoryImage.objects.all() 
    serializer_class=CategoryImageSerializer
    permission_classes= [IsAuthenticated]
    
    def get_queryset(self):
       return self.queryset.filter(category_id=self.kwargs['category_id']) 
    def get(self,request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self,request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
   
    