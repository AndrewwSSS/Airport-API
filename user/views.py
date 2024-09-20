from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from user.serializers import UserCreateSerializer


class CreateUserView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)
