from rest_framework import serializers
from .models import Product,Category,SubCategory,Comments,Favorite, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'uploaded_at']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id', 'tailor', 'Subcategory', 'category', 'title', 'shortdis',
            'description', 'location', 'price', 'created_at', 'updated_at', 'images'
        ]

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        if len(images_data) < 1 or len(images_data) > 5:
            raise serializers.ValidationError("You must upload between 1 and 5 images.")
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            ProductImage.objects.create(product=product, image=image_data)
        return product

    def update(self, instance, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        if len(images_data) < 1 or len(images_data) > 5:
            raise serializers.ValidationError("You must upload between 1 and 5 images.")

        instance = super().update(instance, validated_data)

        # Remove old images if new ones are provided
        if images_data:
            instance.images.all().delete()
            for image_data in images_data:
                ProductImage.objects.create(product=instance, image=image_data)

        return instance

class SubCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']



class FavoriteSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Favorite
        fields = ['product']

    def validate(self, attrs):
        # Ensure the user is adding a favorite for themselves
        if 'user' not in attrs:
            raise serializers.ValidationError('User is required.')
        return attrs

