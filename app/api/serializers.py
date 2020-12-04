from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Restaurant, Order, Comment, OrderDetail, Address, MenuItem, CategoryType, District
from django.contrib.auth import get_user_model # If used custom user model

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)
    class Meta:
        model = UserModel
        fields = ( "id", "username", "password",'email')


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
    user_name = serializers.SerializerMethodField('get_username')
    class Meta:
        model = Comment
        fields = ('title', 'content', 'user_name', 'rating', 'created_at')

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