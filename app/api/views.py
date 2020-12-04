from rest_framework import viewsets, status, permissions, pagination, filters, generics
from .serializers import UserSerializer, RestaurantSerialiser, OrderSerialiser, CommentSerialiser, AddressSerialiser, MenuItemSerialiser, CategoryTypeSerialiser, DistrictSerialiser
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Restaurant, Address, Order, OrderDetail, Comment, OrderDetail, Address, MenuItem, CategoryType, District
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrStaff, IsStaff
from .utils import get_address_func
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer

class Pagination(pagination.PageNumberPagination):
    page_size = 40


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


class OrderListView(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = RestaurantSerialiser
    permission_classes = (
        permissions.AllowAny,)

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        if not self.request.user.is_staff:
            queryset = Order.objects.filter(user_id=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request):
        queryset = Order.objects.filter(user_id=self.request.user)
        serializer = OrderSerialiser(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderSerialiser(data=request.data)
        if (serializer.is_valid() and
            (self.request.user.id == int(request.data['user_id']) or
             self.request.user.is_staff)):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Order.objects.all()
        address = get_object_or_404(queryset, pk=pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def update(self, request, pk=None):
        order = self.get_object()
        serializer = OrderSerialiser(
            order, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order = self.get_object()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderDetailListView(viewsets.ModelViewSet):

    queryset = OrderDetail.objects.all()
    serializer_class = RestaurantSerialiser
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
        serializer = OrderDetailSerialiser(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderDetailSerialiser(data=request.data)
        if (serializer.is_valid() and
            (self.request.user.id == int(request.data['user_id']) or
             self.request.user.is_staff)):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = OrderDetail.objects.all()
        address = get_object_or_404(queryset, pk=pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def update(self, request, pk=None):
        orderDetail = self.get_object()
        serializer = OrderDetailSerialiser(
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
        serializer.save()

    def list(self, request):
        restaurant = self.request.query_params.get('restaurant_id')
        if restaurant is not None:
            queryset = Comment.objects.filter(restaurant_id=restaurant)
            serializer = CommentSerialiser(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = CommentSerialiser(data=request.data)
        if (serializer.is_valid() and
            (self.request.user.id == int(request.data['user_id']) or
             self.request.user.is_staff)):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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