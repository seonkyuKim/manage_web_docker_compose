from django.shortcuts import render

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from .models import Address, Restaurant, Review, SalesInfo
from .serializers import RestaurantSerializer, ReviewSerializer, RestaurantListSerializer


class CannotDestroyViewSet(mixins.CreateModelMixin, 
                            mixins.RetrieveModelMixin, 
                            mixins.UpdateModelMixin, 
                            mixins.ListModelMixin, 
                            viewsets.GenericViewSet):
    """
    This viewset does not support delete method
    """
    pass
    

class ReviewViewSet(CannotDestroyViewSet):
    """
    리뷰와 관련된 API 입니다.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status',]


# # Callables may also be defined out of the class scope.
# def filter_not_empty(queryset, name, value):
#     lookup = '__'.join([name, 'isnull'])
#     return queryset.filter(**{lookup: False})

class RestaurantFilter(filters.FilterSet):
    no_sales_info = filters.BooleanFilter(field_name='sales_info', lookup_expr='isnull')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Restaurant
        fields = ['name', 'status', 'no_sales_info', 'address', ]

# Create your views here.
class RestaurantViewSet(mixins.CreateModelMixin, 
                            mixins.RetrieveModelMixin, 
                            mixins.UpdateModelMixin, 
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RestaurantFilter


class RestaurantListViewSet(mixins.ListModelMixin, 
                            viewsets.GenericViewSet):
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RestaurantFilter