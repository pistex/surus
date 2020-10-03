import json
# import datetime
from django.contrib import auth
from django.contrib.auth.models import Group
from rest_framework.permissions import AllowAny, IsAdminUser
from allauth.account.models import EmailAddress
from rest_framework import decorators
from rest_framework import response
from rest_framework import exceptions
from rest_framework import viewsets
from rest_framework import serializers
User = auth.get_user_model()
create_update_destroy = ['create', 'update', 'partial_update', 'destroy']

@decorators.api_view(['GET'])
def hello_world(request):
    return response.Response({"message": "Hello, world!"})


@decorators.api_view(['GET'])
def all_user(request):
    all_user_objects = User.objects.all()
    all_users = []
    for user in all_user_objects:
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        # permissions = []
        # Permission controller is not needed here because it is already control by RBAC.
        # for permission in user.user_permissions.all():
        #     permissions.append(permission.name)
        allauth_email_verification = EmailAddress.objects.filter(
            email=user.email)
        verified = None
        if len(allauth_email_verification) == 0:
            verified = 'The user does not need verrification.'
        else:
            verified = allauth_email_verification[0].verified
        user_data = {
            'id': user.id,
            # 'profile_picture': user.profile_picture.name,
            'username': user.username,
            # 'password': user.password,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'verified': verified,
            'groups': groups,
            # 'permission': permissions,
            'is_superuser': user.is_superuser,
            # 'is_staff': user.is_staff,
            'is_active': user.is_active,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S')\
                if user.last_login else 'never logged in'
        }
        all_users.append(user_data)
    json_string = json.dumps(all_users)
    return response.Response(json.loads(json_string))


@decorators.api_view(['POST'])
def delete_user(request):
    print(request.data)
    user_obj = User.objects.get(id=request.data['id'])
    username = user_obj.username
    user_obj.delete()
    return response.Response({'deleted user': username})


@decorators.api_view(['GET'])
def user_detail(request, user_id):
    user = User.objects.filter(id=user_id)
    if len(user) == 0:
        raise exceptions.ParseError('No user with this id.')
    user = user[0]
    groups = []
    for group in user.groups.all():
        groups.append(group.name)
    allauth_email_verification = EmailAddress.objects.filter(
        email=user.email)
    verified = None
    if len(allauth_email_verification) == 0:
        verified = 'The user does not need verrification.'
    else:
        verified = allauth_email_verification[0].verified
    user_data = {
        'id': user.id,
        'profile_picture': user.profile_picture.name,
        'username': user.username,
        'password': user.password,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'verified': verified,
        'groups': groups,
        # 'permission': permissions,
        'is_superuser': user.is_superuser,
        # 'is_staff': user.is_staff,
        'is_active': user.is_active,
        'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else 'never logged in'
    }
    json_string = json.dumps(user_data)
    return response.Response(json.loads(json_string))


@decorators.api_view(['POST'])
def update_user_groups(request, user_id):
    user = User.objects.filter(id=user_id)
    if len(user) == 0:
        raise exceptions.ParseError('No user with this id.')
    user = user[0]
    user.groups.clear()
    for group_name in request.data:
        group_object = Group.objects.get(name=group_name)
        user.groups.add(group_object)
    user.save()
    return response.Response({"message": "Hello, world!"})
    
class GroupModelController(viewsets.ModelViewSet):
    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = Group
            fields = '__all__'
    queryset = Group.objects.all()
    serializer_class = Serializer

    # def get_permissions(self):
    #     if self.action in create_update_destroy:
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [AllowAny]
    #     return [permission() for permission in permission_classes]
