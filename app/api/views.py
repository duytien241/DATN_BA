from rest_framework import viewsets, status, permissions, pagination, filters, generics
from .serializers import UserSerializer, RestaurantSerialiser, OrderSerializer, CommentSerialiser, AddressSerialiser, MenuItemSerialiser, CategoryTypeSerialiser, DistrictSerialiser, OrderDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Restaurant, Address, Order, OrderDetail, Comment, OrderDetail, Address, MenuItem, CategoryType, District
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrStaff, IsStaff
from .utils import get_address_func
from utils.common import calculateFeeShip
from rest_framework.generics import CreateAPIView
from json import loads
from django.contrib.auth import get_user_model
User = get_user_model()

class Pagination(pagination.PageNumberPagination):
    page_size = 40

class SearchAPI(APIView):
    pagination_class = Pagination

    def get(self, request):
        text = request.query_params.get('text')
        list = Restaurant.objects.filter(name__icontains= text)
        return JsonResponse({'message': "feeShip"}, status=status.HTTP_401_UNAUTHORIZED)
    
class RestauranFilter(APIView):
    pagination_class = Pagination

    def get(self, request):
        arr = request.query_params.get('arr').split(',')
        list = Restaurant.objects.filter(id__in = arr)
        serializer = RestaurantSerialiser(list)
        return Response({"content":list,"type":'a'})

class FeeShip(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(self)
        location = request.GET['location']
        restaurant = request.GET['restaurant']
        feeShip = calculateFeeShip(location, restaurant)
        return JsonResponse({'message': feeShip}, status=status.HTTP_401_UNAUTHORIZED)

class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

class ChangePassword(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password1")
            rx = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')
            if not self.object.check_password(old_password):
                return Response({"message": "Sai mật khẩu"}, 
                                status=status.HTTP_400_BAD_REQUEST)
            if  rx.match(new_password) is None:
                return Response({"message": "Mật khẩu mới không hợp lệ"}, 
                                status=status.HTTP_400_BAD_REQUEST)
            validate_password(password = new_password, user=self.request.user )
            self.object.set_password(serializer.data.get("new_password1"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditIformationUser(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, pk=None):
        queryset = User.objects.filter(pk=pk)
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if (serializer.is_valid() and (self.request.user.is_staff or self.request.user == user)):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = User.objects.filter(pk=pk)
        user = get_object_or_404(queryset, pk=pk)
        if self.request.user.is_staff or self.request.user == user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return JsonResponse({'message':'Bạn không có quyền truy cập!'}, status=status.HTTP_401_UNAUTHORIZED)

class Users(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    pagination_class = None
    queryset = User.objects.all()



class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer

class RestaurantListView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerialiser
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ['rating', 'cost', 'name']
    filterset_fields = ['rating', 'category_type']
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsStaff,)

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save()


class RestaurantListView2(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerialiser
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ['rating', 'cost', 'name']
    filterset_fields = ['rating', 'category_type']
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsStaff,)

    def get_queryset(self):
        if self.request.query_params.get('arr'):
            arr = self.request.query_params.get('arr').split(',')
            queryset = Restaurant.objects.filter(id__in=arr)
        else:
            text = self.request.query_params.get('text')
            queryset = Restaurant.objects.filter(name__icontains= text)
        return queryset

    def perform_create(self, serializer):
        serializer.save()


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerialiser
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ['rating', 'cost', 'name']
    filterset_fields = ['rating', 'category_type']
    permission_classes = (IsStaff,)


# class RestaurantListView(viewsets.ModelViewSet):

#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerialiser
#     pagination_class = Pagination
#     filter_backends = (DjangoFilterBackend,
#                        filters.SearchFilter, filters.OrderingFilter)
#     ordering_fields = ['rating', 'cost', 'name']
#     filterset_fields = ['rating', 'category_type']
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly, IsStaff,)

#     def get_queryset(self):
#         district = self.request.query_params.get('district')
#         category = self.request.query_params.get('category')
#         ordering = self.request.query_params.get('ordering')
#         queryset = Restaurant.objects.all()
#         # if category is not None:
#         #     queryset = Restaurant.objects.all()
#         if ordering in ['rating', 'cost', 'name']:
#             queryset.annotate('-rating')
#         return queryset

#     def perform_create(self, serializer):
#         serializer.save()

#     def list(self, request):
#         queryset = self.get_queryset()
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = RestaurantSerialiser(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = RestaurantSerialiser(data=request.data)
#         if (serializer.is_valid() and
#                 self.request.user.is_staff):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         queryset = Restaurant.objects.all()
#         restaurant = get_object_or_404(queryset, pk=pk)
#         serializer = RestaurantSerialiser(restaurant)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         restaurant = self.get_object()
#         serializer = RestaurantSerialiser(
#             restaurant, data=request.data, partial=True)
#         if (serializer.is_valid()):
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, pk=None):
#         restaurant = self.get_object()
#         restaurant.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class OrderDetailList(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    queryset = OrderDetail.objects.all()

    def list(self, request):
        queryset = OrderDetail.objects.all()
        serializer = OrderDetailSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = OrderDetailSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, order=None):
        queryset = OrderDetail.objects.filter(order=order)
        serializer = OrderDetailSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        address = self.get_object()
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderHeader(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    pagination_class = None
    queryset = Order.objects.all()
    permission_classes = (
        permissions.IsAuthenticated, IsOwnerOrStaff,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user )

class OrderHeaderShop(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    pagination_class = None
    queryset = Order.objects.all()
    permission_classes = (
        permissions.IsAuthenticated, IsOwnerOrStaff,)

    def get_queryset(self):
        return Order.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user )    
# class OrderListView(viewsets.ModelViewSet):

#     queryset = Order.objects.all()
#     serializer_class = RestaurantSerialiser
#     permission_classes = (
#        IsOwnerOrStaff)

#     def get_queryset(self):
#         queryset = Restaurant.objects.all()
#         if not self.request.user.is_staff:
#             queryset = Order.objects.filter(user_id=self.request.user)
#         return queryset

#     def perform_create(self, serializer):
#         serializer.save()

#     def list(self, request):
#         queryset = Order.objects.filter(user_id=self.request.user)
#         serializer = OrderSerialiser(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = OrderSerialiser(data=request.data)
#         if (serializer.is_valid() and
#             (self.request.user.id == int(request.data['user_id']) or
#              self.request.user.is_staff)):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         queryset = Order.objects.all()
#         address = get_object_or_404(queryset, pk=pk)
#         serializer = AddressSerializer(address)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         order = self.get_object()
#         serializer = OrderSerialiser(
#             order, data=request.data, partial=True)
#         if (serializer.is_valid()):
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, pk=None):
#         order = self.get_object()
#         order.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class OrderDetailListView(viewsets.ModelViewSet):

    queryset = OrderDetail.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsOwnerOrStaff,)

    def get_queryset(self):
        queryset = OrderDetail.objects.filter(order=self.kwargs['order_id'])
        if not self.request.user.is_staff:
            queryset = OrderDetail.objects.filter(user_id=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request):
        queryset = OrderDetail.objects.filter(user_id=self.request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if (serializer.is_valid() and
            (self.request.user.id == int(request.data['user_id']) or
             self.request.user.is_staff)):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = OrderDetail.objects.all()
        address = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(address)
        return Response(serializer.data)

    def update(self, request, pk=None):
        orderDetail = self.get_object()
        serializer = OrderSerialiser(
            orderDetail, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        orderDetail = self.get_object()
        orderDetail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListView(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerialiser
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Comment.objects.filter(
            restaurant_id=self.kwargs['restaurant_id'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user )

    def list(self, request):
        restaurant = self.request.query_params.get('restaurant_id')
        if restaurant is not None:
            queryset = Comment.objects.filter(restaurant_id=restaurant)
            serializer = CommentSerialiser(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Comment.objects.all()
        address = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerialiser(address)
        return Response(serializer.data)

    def update(self, request, pk=None):
        comment = self.get_object()
        serializer = CommentSerialiser(
            comment, data=request.data, partial=True)
        if (serializer.is_valid() and self.request.user.id == int(request.data['user_id'])):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddressView(generics.ListCreateAPIView):
    serializer_class = AddressSerialiser
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsStaff,)

    def get_queryset(self):
        address = Address.objects.filter(
            restaurant_id=self.kwargs['restaurant_id'])
        return address

    def perform_create(self, serializer):
        address = get_object_or_404(
            Address, restaurant_id=self.kwargs['restaurant_id'])
        serializer.save(project=project)

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerialiser
    pagination_class = Pagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        print(self.kwargs['restaurant_id'])
        queryset = Comment.objects.filter(
            restaurant_id=self.kwargs['restaurant_id'])
        return queryset

    def perform_create(self, serializer):
        serializer.save()

class MenuListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerialiser
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    # ordering_fields = ['rating', 'cost', 'name']
    # filterset_fields = ['rating', 'category_type']
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = MenuItem.objects.filter(
            restaurant_id=self.kwargs['restaurant_id'])
        return queryset

    def perform_create(self, serializer):
        serializer.save()

class CategoryTypeListView(generics.ListCreateAPIView):
    queryset = CategoryType.objects.all()
    serializer_class = CategoryTypeSerialiser
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = CategoryType.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save()

class ListShopWithType(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerialiser
    pagination_class = Pagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Restaurant.objects.filter(
            category_type_id=self.kwargs['food_type_id'])
        return queryset

    def perform_create(self, serializer):
        serializer.save()

class ListDistrict(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerialiser
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = District.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save()

