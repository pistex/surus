from django.contrib import auth
from allauth.account.models import EmailAddress
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import mixins
from .permissions import IsUser
User = auth.get_user_model()
create_update_destroy = ['create', 'update', 'partial_update', 'destroy']


class ProfileController(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'profile_picture', 'username',
                      'email', 'first_name', 'last_name', 'date_joined', 'last_login')
            read_only_fields = ('id', 'date_joined', 'last_login')
    queryset = User.objects
    serializer_class = Serializer
    # permission_classes = [IsUser]
