from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Restaurant, Order, Comment, OrderDetail, Address, MenuItem, CategoryType, District, User, Sale
from django.contrib.auth import get_user_model # If used custom user model
from django.http import JsonResponse
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    # phone = serializers.SerializerMethodField('get_phone')
    # address = serializers.SerializerMethodField('get_address')
    restaurant = serializers.SerializerMethodField('get_restaurant')
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email','password','phone', 'address', 'role', 'restaurant')
        read_only_fields = ('id', 'username')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.username = user.email
        user.save()
        return user

    def get_restaurant(self, obj):
        try:
            restaurant = Restaurant.objects.get(user = obj)
        except User.DoesNotExist:
            restaurant = None
        if restaurant:
            return restaurant.id
        return None

    # def get_address(self, obj):
    #     try:
    #         userInfo = User.objects.get(user = obj)
    #     except User.DoesNotExist:
    #         userInfo = None
    #     if userInfo:
    #         return userInfo.address
    #     return None
    # def get_role(self, obj):
    #     try:
    #         userInfo = User.objects.get(user = obj)
    #     except User.DoesNotExist:
    #         userInfo = None
    #     if userInfo:
    #         return userInfo.role
    #     return 2

class PasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        password1 = attrs['new_password1']
        password2 = attrs['new_password2']
        if password1 != password2:
            raise ValidationError('Hai mật khẩu không giống nhau.')
        return attrs


class RestaurantSerialiser(serializers.ModelSerializer):
    address = serializers.SerializerMethodField('get_address')
    time = serializers.SerializerMethodField('get_time_open')
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'uri', 'cost', 'rating', 'description',
                  'phone', 'image_url', 'category_type', 'has_pre_order',
                  'category_domain', 'category_type', 'trademark', 'time','address')
    
    def get_address(self, obj):
        address = Address.objects.get(restaurant_id = obj.id)
        if address is not None:
            return (address.address_full, address.location_lat, address.location_lng)
        return ''

    def get_time_open(self, obj):
        time = obj.time_open
        if time.has_two_shift:
            return time.shift_one_start + "-" + time.shift_one_end + "|" +time.shift_two_start + "-" + time.shift_two_end
        else:
            return time.shift_one_start + "-" + time.shift_one_end

class OrderDetailSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField('get_item', read_only=True,)
    class Meta:
        model = OrderDetail
        fields = ('id', 'quantity','order', 'item','menu_item')
    
    def get_item(self, obj):
        return obj.menu_item.name
class OrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(many=True, read_only=True,)
    username = serializers.SerializerMethodField('get_username', read_only=True,)
    class Meta:
        model = Order
        fields = ('id', 'restaurant', 'user', 'username', 'time_order', 'total_cost', 'address_ship', 'phone',
                  'note', 'status', 'order_detail')

    def get_username(self, obj):
        return obj.user.username


class PreOrderSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('restaurant', 'user', 'time_order', 'total_cost', 'address_ship', 'phone',
                  'note', 'user_email', 'status')


class CommentSerialiser(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField('get_username')
    class Meta:
        model = Comment
        fields = ('title', 'content', 'user_name', 'rating', 'restaurant')

    def get_username(self, obj):
        return obj.user.username


class AddressSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class MenuItemSerialiser(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class CategoryTypeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = CategoryType
        fields = '__all__'

class DistrictSerialiser(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class SaleSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

class OrderSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','status')