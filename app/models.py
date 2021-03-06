from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import date

class TradeMark(models.Model):
    name = models.CharField(max_length=200)
    uri = models.CharField(max_length=200)
    number_store = models.IntegerField(default=0)


class CategoryType(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.TextField(null=True,blank=True,)

class CategoryDomain(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.TextField(null=True,blank=True,)


class District(models.Model):
    district = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    class Meta:
        unique_together = ('district', 'city')


class TimeOpen(models.Model):
    shift_one_start = models.CharField(max_length=10)
    shift_one_end = models.CharField(max_length=10)
    shift_two_start = models.CharField(max_length=10)
    shift_two_end = models.CharField(max_length=10)
    has_two_shift = models.BooleanField(default=False)


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    uri = models.CharField(max_length=200)
    cost = models.TextField()
    rating = models.FloatField(default=0)
    description = models.TextField()
    phone = models.CharField(max_length=13)
    image_url = models.TextField(null=True,blank=True,)
    has_pre_order = models.BooleanField(default=False,null=True,blank=True,)
    category_type = models.ForeignKey(CategoryType,
                                      related_name="CategoryType",
                                      on_delete=models.CASCADE,
                                      null=True,
                                      blank=True,)
    category_domain = models.ForeignKey(CategoryDomain,
                                        related_name="CategoryDomain",
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True,)
    trademark = models.ForeignKey(TradeMark,
                                 related_name="trademark",
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True,
                                 )
    time_open = models.ForeignKey(TimeOpen,
                                  related_name="time_open",
                                  on_delete=models.CASCADE,
                                  null=True,
                                  blank=True,)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="owned",
        on_delete=models.CASCADE,
    )

class Sale(models.Model):
    restaurant = models.ForeignKey(Restaurant,
                                   related_name="sale_restaurant",
                                   on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date = models.DateField(default=date.today)  
    discount = models.FloatField(default=0)

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant,
                                   related_name="menu_restaurant",
                                   on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    total_order = models.IntegerField(default=0)
    price = models.TextField()
    image_url = models.TextField()

class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant,
                                   related_name="order_restaurant",
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    time_order = models.CharField(max_length=200)
    total_cost = models.IntegerField(default=0)
    address_ship = models.CharField(max_length=200,null=True,blank=True,)
    phone = models.CharField(max_length=10,null=True,blank=True)
    note = models.CharField(max_length=200,null=True,blank=True)
    user_email = models.CharField(max_length=200)
    status = models.CharField(max_length=200)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order,
                              related_name="order_detail",
                              on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem,
                                  related_name="menu_order",
                                  on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class PreOrder(models.Model):
    restaurant = models.ForeignKey(Restaurant,
                                   related_name="preorder_restaurant",
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    address_ship = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    user_email = models.CharField(max_length=200)
    time_order = models.CharField(max_length=10)
    note = models.CharField(max_length=200)
    type_table = models.CharField(max_length=200)
    number_people = models.IntegerField(default=0)


class Address(models.Model):
    restaurant = models.ForeignKey(Restaurant,
                                   related_name="address_restaurant",
                                   on_delete=models.CASCADE)
    address_full = models.CharField(max_length=200)
    street_number = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    distance = models.FloatField(default=0)
    location_lat = models.FloatField(default=0,null=True,blank=True,)
    location_lng = models.FloatField(default=0,null=True,blank=True,)
    district = models.ForeignKey(District,
                                 related_name="district_store",
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True,)


class Comment(models.Model):
    restaurant = models.ForeignKey(Restaurant,
                                   related_name="comment_restaurant",
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,)
    title = models.TextField()
    content = models.TextField()
    created_at = models.CharField(max_length=20)
    rating = models.FloatField(default=0)


class User(AbstractUser):
    phone = models.CharField(max_length=20,null=True, blank=True)
    birthday = models.CharField(max_length=20,null=True, blank=True)
    avatar = models.TextField(null=True, blank=True)
    role = models.IntegerField(default=2)
    address = models.TextField(null=True, blank=True)
