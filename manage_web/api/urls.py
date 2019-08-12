
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'restaurants', views.RestaurantListViewSet, base_name='restaurants')
router.register(r'restaurants', views.RestaurantViewSet, base_name='restaurants')
router.register(r'reviews', views.ReviewViewSet, base_name='reviews')



# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
app_label = 'api'

urlpatterns = [
    path('', include(router.urls)),
]




