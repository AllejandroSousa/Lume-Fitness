from django.urls import path
from . import views

urlpatterns = [
    path('admin_page/merchandise/', views.admin_merchandise, name='admin_merchandise'),
    path('admin_page/merchandise/', views.admin_merchandise, name='admin_merchandise'),
    path('admin_page/edit-product/<slug:slug>/', views.edit_product, name='edit_product'),
    path('admin_page/delete-product/<slug:slug>/', views.delete_product, name='delete_product'),
    path('admin_page/edit-category/<slug:slug>/', views.edit_category, name='edit_category'),
    path('admin_page/delete-category/<slug:slug>/', views.delete_category, name='delete_category'),

    path('', views.store, name='store'),
    path('product/<slug:product_slug>/', views.product_info, name='product-info'),
    path('search/<slug:category_slug>/', views.list_category, name='list-category'),

    path('search/', views.search_results, name='search_results'),

]