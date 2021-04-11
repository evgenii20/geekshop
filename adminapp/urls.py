from django.urls import path
from adminapp import views as adminapp

# с версии 2.0 app_name
app_name = 'adminapp'

urlpatterns = [
    # CRUD
    path('users/create/', adminapp.user_create, name='user_create'),
    # path( 'users/read/' , adminapp.users, name= 'users' ),
    # path('users/read/', adminapp.users, name='users_read'),
    # path('users/read/', adminapp.user_read, name='user_read'),
    # path('users/read/', adminapp.UsersListView.as_view(), name='users'),
    path('users/read/', adminapp.UsersListView.as_view(), name='user_read'),
    path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    # path('users/update/<int:pk>/', adminapp.UsersUpdateView, name='user_update'),
    path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),

    # path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    # path( 'categories/read/' , adminapp.categories, name= 'categories' ),
    # path('categories/read/', adminapp.categories, name='category_read'),
    path('categories/read/', adminapp.ProductCategoriesListView.as_view(), name='category_read'),
    # path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    # path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    path('categories/delete/<int:pk>/', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),

    # path('products/create/category/<int:pk>/', adminapp.product_create, name='product_create'),
    path('products/create/category/<int:pk>/', adminapp.ProductCreateView.as_view(), name='product_create'),
    # Первый выводит список продуктов в категории
    # path('products/read/category/<int:pk>/', adminapp.products, name='products'),
    path('products/read/category/<int:pk>/', adminapp.ProductListView.as_view(), name='products'),
    # а второй — страницу выбранного продукта
    # path('products/read/<int:pk>/', adminapp.product_read, name='product_read'),
    path('products/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),
    # path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('products/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    # path('products/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
    path('products/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),
]