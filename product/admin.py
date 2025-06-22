from django.contrib import admin
from .models import Category, SubCategory, Product, Comments, ProductImage

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Comments)
admin.site.register(ProductImage)