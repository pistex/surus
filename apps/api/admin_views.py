from django.contrib import auth
from django.contrib.auth.models import Group
from rest_framework import decorators
from rest_framework import response
from rest_framework import serializers
User = auth.get_user_model()

@decorators.api_view()
def hello_world(request):
    return response.Response({"message": "Hello, world!"})
