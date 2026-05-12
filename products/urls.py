from django.urls import path
from .views import (
    products_view,
    categories_view,
    add_products_view,
    add_category_view,
    product_detail_view,
    category_detail_view,
    delete_category,
    delete_product,
    PostUser,
    GetUserViews
)

urlpatterns = [
    path("products/", products_view, name="products"),
    path("categories/", categories_view, name="categories"),
    path("products/add/", add_products_view, name="add_product"),
    path("categories/add/", add_category_view, name="add_category"),
    path("products/<int:pk>", product_detail_view, name="product_detail_view"),
    path("categories/<int:pk>", category_detail_view, name="category_detail_view"),
    path("categories/delete/<int:pk>/", delete_category, name="delete_category"),
    path("products/delete/<int:pk>/", delete_product, name="delete_product"),
    path("user/", PostUser, name="user"),
    path('alluser/', GetUserViews, name="alluser")
]
