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
from django.urls import path, include
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

# order_list = views.OrderListView.as_view({
#     'get': 'list',
#     'post': 'create'
# })
order_detail = views.OrderDetailList.as_view({
    'post': 'create',
    'get': 'list',
})


order_detail_id = views.OrderDetailListView.as_view({
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

user_detail = views.EditIformationUser.as_view({
    'get': 'retrieve',
    'put': 'update',
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
    path('me', views.Me.as_view(), name='me'),
    path('logout/', views.Logout.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('users', views.Users.as_view(), name='users-list'),
    path('user/<int:pk>/', user_detail, name='user-detail'),
    path('user/changepassword/', views.ChangePassword.as_view(), name='change-password'),
    path('api/feeship', views.FeeShip.as_view(), name='fee-ship'),
    path('api/restaurant/', views.RestaurantListView.as_view(),
         name='restaurant-list'),
    path('api/restaurant/<int:pk>/',
         views.RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('api/order/', order_detail, name='order_detail'),
    path('api/order/<int:order>/', order_detail_id, name='order_detail_id'),
    path('api/comment/', comment_list, name='comment-list'),
    path('api/comment/<int:restaurant_id>/',
         views.CommentView.as_view(), name='menu-detail'),
    path('api/orders/', views.OrderHeader.as_view(), name='order-list'),
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
    path('api/user/register',
         views.CreateUserView.as_view(), name='create-user'),
]
