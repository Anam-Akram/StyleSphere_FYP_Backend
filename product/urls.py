from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'subcategory', SubViewSet, basename='subcategory')
router.register(r'category', CatViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('categoryProducts/', get_cat_products_data, name='get_cat_products_data'),
path('favorites/', FavoriteProductListView.as_view(), name='favorite-product-list'),
    path('favorites/add/', add_to_favorites, name='add-to-favorites'),
    path('favorites/remove/', remove_from_favorites, name='remove-from-favorites'),
]
