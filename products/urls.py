
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('category_products/',views.ajax_category_view,name='detail_category'),
    # path('ajax_view/',views.ajax_view,name='ajax'),
    path('home/',views.home,name='home' ),
    path('',views.home,name='products' ),
    path('<slug:category_slug>/',views.home,name='home_category'),
    path('product/<slug:slug>/',views.product_detail,name='product_detail'),
    path('search',views.search,name='search'),



]
