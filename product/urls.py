#==>Library Import
from django.urls import path
from . import views


app_name='product'
urlpatterns = [
    path('navbar/', views.NavbarView.as_view(), name='navbar'),
    path('', views.HomeView.as_view(), name='home'),
    path('product/<slug:slug>/', views.ProductDetail.as_view(), name='detail'),
    path('category/<slug:slug>/', views.ProductCategoryList.as_view(), name='category'),
    path('product-list/', views.ProductListView.as_view(), name='product_list'),
    path('about-us/', views.AboutUs.as_view(), name='about-us'),
    path('contact-us/', views.ContactUs.as_view(), name='contact-us'),
]

