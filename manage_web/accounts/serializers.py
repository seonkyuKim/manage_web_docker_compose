from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_writable_nested import WritableNestedModelSerializer

from accounts.models import (
    Reviewer, Editor, User
)
from api.models import (
    Review
)

class EditorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Editor
        fields = ['name', 'phone_number']


class ReviewSerializerForReviewer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.__str__')
    restaurant_image = serializers.ImageField(source='restaurant.image')

    class Meta:
        model = Review
        fields = ['id', 'restaurant_name', 'register_time', 'status', 'restaurant_image']


class ReviewerSerializer(WritableNestedModelSerializer):
    editor = EditorSerializer()
    review_set = ReviewSerializerForReviewer(many=True)

    class Meta:
        model = Reviewer
        exclude = []



class UserSerializer(WritableNestedModelSerializer):
    reviewer = ReviewerSerializer()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'reviewer']
