"""webping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# restaurant_list = views.RestaurantListView.as_view({
#     'get': 'list',
#     'post': 'create'
# })

# restaurant_detail = views.RestaurantListView.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'delete': 'destroy'
# })

order_list = views.OrderListView.as_view({
    'get': 'list',
    'post': 'create'
})

order_detail = views.OrderListView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

comment_list = views.CommentListView.as_view({
    'get': 'list',
    'post': 'create'
})

comment_detail = views.CommentListView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

order_detail_list = views.OrderDetailListView.as_view({
    'get': 'list',
    'post': 'create'
})

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/restaurant/', views.RestaurantListView.as_view(),
         name='restaurant-list'),
    path('api/restaurant/<int:pk>/',
         views.RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('api/order/', order_list, name='order-list'),
    path('api/order/<int:pk>/', order_detail, name='order-detail'),
    path('api/comment/', comment_detail, name='comment-list'),
    path('api/comment/<int:restaurant_id>/',
         views.CommentView.as_view(), name='menu-detail'),
    path('api/order-details/<int:order_id>',
         order_detail_list, name='order-detail-list'),
    path('api/address/<int:restaurant_id>/',
         views.AddressView.as_view(), name='address-detail'),
    path('api/menu/<int:restaurant_id>/',
         views.MenuListView.as_view(), name='menu-detail'),
    path('api-docs', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-redoc'),
    path('api/foodtype/',
         views.CategoryTypeListView.as_view(), name='food-type-list'),
    path('api/foodtype/<int:food_type_id>/',
         views.ListShopWithType.as_view(), name='list-food-type'),
    path('api/district/',
         views.ListDistrict.as_view(), name='list-district'),
]
