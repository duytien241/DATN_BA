from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Restaurant, Order, Comment, OrderDetail, Address, MenuItem


class UserSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class RestaurantSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'uri', 'cost', 'rating', 'description',
                  'phone', 'image_url', 'category_type', 'has_pre_order',
                  'category_domain', 'category_type', 'trademark', 'time_open')


class OrderSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('restaurant', 'user', 'time_order', 'total_cost', 'address_ship', 'phone',
                  'note', 'user_email', 'status')


class OrderDetailSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'


class PreOrderSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('restaurant', 'user', 'time_order', 'total_cost', 'address_ship', 'phone',
                  'note', 'user_email', 'status')


class CommentSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class AddressSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class MenuItemSerialiser(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
