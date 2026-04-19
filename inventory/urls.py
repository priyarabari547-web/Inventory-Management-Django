from django.urls import path
from django.contrib.auth import views as auth_views  
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('add-product/', views.add_product, name='add_product'),
    path('update-product/<int:id>/', views.update_product, name='update_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
    path('add-sale/', views.add_sale, name='add_sale'),
    path('adjust-stock/', views.stock_adjustment, name='stock_adjustment'),
    
]