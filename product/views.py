from django.http import JsonResponse
from requests import Response
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny
from .models import Product,Comments,SubCategory,Category,Favorite
from .serializers import ProductSerializer,CommentsSerializer,SubCatSerializer,CatSerializer,FavoriteProductSerializer,FavoriteSerializer
from User.models import UserAccount
from rest_framework import status
from rest_framework.response import Response


class FavoriteProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FavoriteProductSerializer

    def get_queryset(self):
        user_id = self.request.data.get('user_id')
        user = UserAccount.objects.get(id=user_id)
        return Product.objects.filter(favorite__user=user)

@api_view(['POST'])
def add_to_favorites(request):
    product_id = request.data.get('product')
    user_id = request.data.get('user_id')
    user = UserAccount.objects.get(id=user_id)
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    if Favorite.objects.filter(user=user, product=product).exists():
        return Response({"detail": "Product is already in your favorites."}, status=status.HTTP_400_BAD_REQUEST)

    favorite = Favorite.objects.create(user=user, product=product)

    return Response(FavoriteSerializer(favorite).data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def remove_from_favorites(request):
    user_id = request.data.get('user_id')
    product_id = request.data.get('product_id')
    user = UserAccount.objects.get(id=user_id)
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


    favorite = Favorite.objects.filter(user=user, product=product).first()
    if not favorite:
        return Response({"detail": "Product is not in your favorites."}, status=status.HTTP_400_BAD_REQUEST)
    favorite.delete()

    return Response({"detail": "Product removed from favorites."}, status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def get_cat_products_data(request):
    try:
        # Extract the category name from the request data
        cat_name = request.data.get('cat_name')
        if not cat_name:
            return JsonResponse(
                {"message": "Category name is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        products = Product.objects.filter(category__name=cat_name)

        if not products.exists():
            return JsonResponse(
                {"message": "No products found for this category."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the products data
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(
            {"message": "Products retrieved successfully.", "data": serializer.data}
        )

    except Exception as e:
        return JsonResponse(
            {"message": "An error occurred.", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        if product_id:
            data = Comments.objects.filter(product=product_id)
            return data
        return super().get_queryset()

    def perform_create(self, serializer,):
        user_id = self.request.POST.get('user')

        user_instance = UserAccount.objects.get(id=user_id)

        serializer.save(user=user_instance)

class CatViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CatSerializer
    permission_classes = [AllowAny]

class SubViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = SubCategory.objects.all()
    serializer_class = SubCatSerializer
    permission_classes = [AllowAny]