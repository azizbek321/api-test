from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .models import Product, Category
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ProductDetailSerializer,
    CategoryDetailSerializer,
    RegisterUserSer,
    AllUserSerializer
)
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView


@api_view(["POST"])
def PostUser(request):
    data = request.data
    serializer = RegisterUserSer(data=data)
    serializer.is_valid(raise_exception=True)
    token = serializer.save()
    return Response(data={"token":f"{token.key}"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def GetUserViews(request):
    # serializer = AllUserSerializer(request.user)
    # return Response(serializer.data)
    users = User.objects.all()
    serializer = AllUserSerializer(data=users, many=True)
    serializer.is_valid()
    return Response(data=serializer.data, status=status.HTTP_200_OK)

# class GetUserViews(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = AllUserSerializer











@api_view(["GET"])
@permission_classes([IsAuthenticated])
def products_view(request):
    page = request.GET.get("page", "1")
    category_id = request.GET.get("category", "")
    search = request.GET.get("search", "")

    start = (int(page) - 1) * 10
    end = start + 10

    if search:
        products = Product.objects.filter(
            Q(name__icontains=search), Q(description__icontains=search)
        )
        serialized_data = ProductSerializer(products, many=True).data
        return Response(data=serialized_data)

    if category_id:
        products = Product.objects.filter(category_id=category_id).all()[start:end]
        serialized_data = ProductSerializer(products, many=True).data
        return Response(data=serialized_data)

    products = Product.objects.all()[start:end]
    serialized_data = ProductSerializer(products, many=True).data
    return Response(data=serialized_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def categories_view(request):
    page = request.GET.get("page", "1")
    start = (int(page) - 1) * 10
    end = start + 10
    products = Category.objects.all()[start:end]
    print(products)
    serialized_data = CategorySerializer(products, many=True).data
    return Response(data=serialized_data)


@api_view(["POST"])
def add_category_view(request):
    if isinstance(request.data, dict):
        new_category = request.data
        Category.objects.create(**new_category)
        return Response(status=status.HTTP_201_CREATED)
    elif isinstance(request.data, list):
        for new_category in request.data:
            Category.objects.create(**new_category)
        return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def add_products_view(request):
    if isinstance(request.data, dict):
        new_product = request.data
        category = Category.objects.get(id=new_product["category"])
        Product.objects.create(
            name=new_product["name"],
            description=new_product["description"],
            price=new_product["price"],
            category=category,
        )
        return Response(status=status.HTTP_201_CREATED)
    elif isinstance(request.data, list):
        for new_product in request.data:
            category = Category.objects.get(id=new_product["category"])
            Product.objects.create(
                name=new_product["name"],
                description=new_product["description"],
                price=new_product["price"],
                category=category,
            )
        return Response(status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        category.delete()
    except Category.DoesNotExist:
        return Response(
            {"error": f"no category was found with id={pk}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(data={"success":"delete category"},status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
# @permission_classes([IsAdminUser])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
    except Product.DoesNotExist:
        return Response(
            {"error": f"no product was found with id={pk}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def product_detail_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serialized_data = ProductDetailSerializer(product).data
        return Response(serialized_data)
    except Product.DoesNotExist:
        return Response(
            {"error": f"no product was found with id={pk}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def category_detail_view(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        serialized_data = CategoryDetailSerializer(category).data
        return Response(serialized_data)
    except Category.DoesNotExist:
        return Response(
            {"error": f"no category was found with id={pk}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
