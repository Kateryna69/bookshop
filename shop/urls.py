from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('book/<slug:slug>/', views.product_detail, name='product_detail'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.wishlist_toggle, name='wishlist_toggle'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('about/', views.about_view, name='about'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/orders/', views.admin_orders, name='admin_orders'),
    path('dashboard/users/', views.admin_users, name='admin_users'),
]