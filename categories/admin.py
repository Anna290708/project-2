from django.contrib import admin
from .models import *

class CategoryInline(admin.TabularInline):
    model=CategoryImage
    extra=1

@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    inlines=[CategoryInline]
    
admin.site.register(CategoryImage)