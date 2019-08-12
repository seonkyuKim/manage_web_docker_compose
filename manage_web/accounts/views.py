from django.shortcuts import render

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from .models import Editor, Reviewer, User
from .serializers import EditorSerializer, ReviewerSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    리뷰어 관련 API 입니다.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email',]


class ReviewerViewSet(viewsets.ModelViewSet):
    """
    Reviewer 관련 API입니다.
    """
    queryset = Reviewer.objects.all()
    serializer_class = ReviewerSerializer