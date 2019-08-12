from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_writable_nested import WritableNestedModelSerializer

from .models import (
    Restaurant, SalesInfo, BreakTime, BusinessHour, LastOrder, LargeCategory, SmallCategory,
    Review, Menu, Food, Days24h, DaysOff,
    MenuImage, MenuBoardImage, InteriorImage, OtherImage, 
)





# Belongs to menu
class MenuImageSerializer(WritableNestedModelSerializer):
    class Meta:
        model = MenuImage
        fields = ['image', 'id']

# Belongs to review
class MenuBoardImageSerializer(WritableNestedModelSerializer):
    class Meta:
        model = MenuBoardImage
        fields = ['image', 'id']

# Belongs to review
class InteriorImageSerializer(WritableNestedModelSerializer):
    class Meta:
        model = InteriorImage
        fields = ['image', 'id']

# Belongs to review
class OtherImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherImage
        fields = ['image', 'id']



########################## Restaurant ###########################

class Days24hSerializer(serializers.ModelSerializer):
    class Meta:
        model = Days24h
        exclude = ['sales_info']

class DaysOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaysOff
        exclude = ['sales_info']



class BreakTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BreakTime
        exclude = ['sales_info']


class BusinessHourSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessHour
        exclude = ['sales_info']


class LastOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = LastOrder
        exclude = ['sales_info']


class SalesInfoSerializer(WritableNestedModelSerializer):
    # Reverse OneToOne relation
    break_time = BreakTimeSerializer()
    business_hour = BusinessHourSerializer()
    last_order = LastOrderSerializer()
    days_off = DaysOffSerializer()
    days_24h = Days24hSerializer()

    class Meta:
        model = SalesInfo
        exclude = []
    


class LargeCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = LargeCategory
        exclude = ()

class SmallCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SmallCategory
        exclude = ()

class RestaurantSerializer(WritableNestedModelSerializer):
    # Reverse OneToOne relation
    sales_info = SalesInfoSerializer(required=False, allow_null=True)

    reviewer_name = serializers.CharField(source='get_reviewer_name', required=False)

    # Reverse FK relation
    largecategory_set = LargeCategorySerializer(required=False, many=True, allow_null=True)
    smallcategory_set = SmallCategorySerializer(required=False, many=True, allow_null=True)

    # longitude and latitude
    longitude = serializers.FloatField(source='get_longitude', required=False)
    latitude = serializers.FloatField(source='get_latitude', required=False)

    # registered review type
    is_restaurant_registered = serializers.BooleanField(required=False)
    is_bar_registered = serializers.BooleanField(required=False)
    is_cafe_registered = serializers.BooleanField(required=False)

    class Meta:
        model = Restaurant
        exclude = ()
        read_only_fields = (
            'registered_time', 
            'longitude', 
            'latitude', 
            'is_restaurant_registered', 
            'is_bar_registered', 
            'is_cafe_registered',
            'reviewer_name',
        )


class RestaurantListSerializer(WritableNestedModelSerializer):
    
    # longitude and latitude
    longitude = serializers.FloatField(source='get_longitude', required=False)
    latitude = serializers.FloatField(source='get_latitude', required=False)

    # registered review type
    is_restaurant_registered = serializers.BooleanField(required=False)
    is_bar_registered = serializers.BooleanField(required=False)
    is_cafe_registered = serializers.BooleanField(required=False)

    reviewer_name = serializers.CharField(source='get_reviewer_name', required=False)

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'branch_name',
            'address',
            'longitude', 
            'latitude',
            'floor',

            'is_restaurant_possible',
            'is_bar_possible',
            'is_cafe_possible',

            'is_restaurant_registered', 
            'is_bar_registered', 
            'is_cafe_registered', 

            'status',
            'registered_time',
            'reviewer',
            'rejected_reason',
            'size',
            'is_duplex',
            'is_room',
            'self_service',
            'is_bar_table',
            'restroom',
            'restroom_cleanliness',
            'image',
            'reviewer_name',
        ]

        read_only_fields = (
            'registered_time', 
            'longitude', 
            'latitude', 
            'is_restaurant_registered', 
            'is_bar_registered', 
            'is_cafe_registered',
            'reviewer_name',
        )

    

########################## Review ###########################


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        exclude = ()

class MenuSerializer(WritableNestedModelSerializer):
    # Reverse FK relation
    food_set = FoodSerializer(many=True, required=False)
    menuimage_set = MenuImageSerializer(many=True)

    class Meta:
        model = Menu
        exclude = ()

class ReviewSerializer(WritableNestedModelSerializer):
    # Reverse FK relation
    menu_set = MenuSerializer(many=True)
    menuboardimage_set = MenuBoardImageSerializer(many=True)
    interiorimage_set = InteriorImageSerializer(many=True)
    otherimage_set = OtherImageSerializer(many=True)

    restaurant_name = serializers.CharField(source='get_restaurant_name', required=False)

    class Meta:
        model = Review
        exclude = ()
