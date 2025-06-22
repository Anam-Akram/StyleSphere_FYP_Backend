from django.db import models
from User.models import UserAccount
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100,null=False)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100,null=False)


    def __str__(self):
        return self.name

from django.db import models

class Product(models.Model):
    tailor = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        limit_choices_to={'is_tailor': True},
        related_name='products'
    )
    Subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    shortdis = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    location = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Product {self.title} by {self.tailor.first_name}'

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image for {self.product.title}'


class Comments(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='user')
    # tailor = models.models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='tailor')
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.first_name} on {self.product.title}'

class Favorite(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevents a user from favoriting the same product twice

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


