import json
from allauth.account.utils import sync_user_email_addresses
from allauth.account.models import EmailAddress, EmailConfirmationHMAC, EmailConfirmation
from allauth.account import signals
from django.contrib import auth
from rest_framework import decorators
from rest_framework import exceptions
from rest_framework import mixins
from rest_framework import response
from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets
from .permissions import IsUser, IsOwner
from .helpers import social_account_check

User = auth.get_user_model()
create_update_destroy = [
    'create',
    'update',
    'partial_update',
    'destroy'
    ]


class ProfileController(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                'id',
                'profile_picture',
                'username',
                'first_name',
                'last_name',
                'date_joined',
                'last_login',
                'is_superuser'
                ]
            read_only_fields = [
                'id',
                'date_joined',
                'last_login',
                'is_superuser'
                ]
    queryset = User.objects.all()
    serializer_class = Serializer
    permission_classes = [IsUser]

    def get_profile(self, user_object):
        serializer = self.get_serializer(user_object)
        allauth_email = EmailAddress.objects.filter(user=user_object)
        groups = []
        for group in user_object.groups.all():
            groups.append(group.name)
        email = []
        social = [
            {'facebook': social_account_check(user_object, 'facebook')},
            {'google': social_account_check(user_object, 'google')}
        ]
        for email_object in allauth_email:
            data = {
                'id': email_object.id,
                'email': email_object.email,
                'primary': email_object.primary,
                'verified': email_object.verified
            }
            email.append(data)
        json_data = json.dumps(serializer.data)[:-1] \
            + ', "email": ' \
            + json.dumps(email) \
            + ', "groups": ' \
            + json.dumps(groups) \
            + ', "social": ' \
            + json.dumps(social) \
            + '}'
        return json_data

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise exceptions.AuthenticationFailed('Authentiucated user only.')
        user_id = request.user.id
        user_object = User.objects.get(id=user_id)
        json_data = self.get_profile(user_object)
        return response.Response(json.loads(json_data),
                                 status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):  # pylint: disable=unused-argument # maintain overriding signature
        user_object = self.get_object()
        json_data = self.get_profile(user_object)
        return response.Response(json.loads(json_data),
                                 status=status.HTTP_200_OK)

class EmailController(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = EmailAddress
            fields = [
                'id',
                'email',
                'primary',
                'verified'
                ]
            read_only_fields = [
                'email',
                'primary',
                'verified'
                ]
    queryset = EmailAddress.objects.all()
    serializer_class = Serializer
    permission_classes = [IsOwner]

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise exceptions.MethodNotAllowed(
                "method PUT is not allow for this endpoint.")
        requested_user = self.initialize_request(request, *args, **kwargs).user
        sync_user_email_addresses(requested_user)
        return super(EmailController, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        signals.email_added.send(
            sender=request.user.__class__,
            request=request,
            user=request.user,
            email_address=request.data["email"])
        created_email = EmailAddress.objects.add_email(
            request=request,
            user=request.user,
            email=request.data["email"],
            confirm=True)
        return response.Response(
            {'created': created_email.email},
            status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        if "verified" in request.data:
            raise exceptions.ParseError(
                'Cannot change verification status on this endpint.')
        if "email" in request.data:
            raise exceptions.ParseError(
                'Cannot change email address on this endpint.')
        if not request.data['primary']:
            raise exceptions.ParseError(
                'This endpoint is for making primary email only')
        try:
            new_primary_email = EmailAddress.objects.get(id=request.data['id'])
            if not new_primary_email.verified:
                raise exceptions.ParseError(
                    'Please verify your email before make it primary')
            try:
                old_primary_email = EmailAddress.objects \
                    .get(user=request.user, primary=True)
            except EmailAddress.DoesNotExist:
                old_primary_email = None
            if new_primary_email == old_primary_email:
                return response.Response(
                    {'detail': 'The email is already primary.'},
                    status=status.HTTP_200_OK)
            new_primary_email.set_as_primary()
            signals.email_changed \
                .send(sender=request.user.__class__,
                      request=request,
                      user=request.user,
                      from_email_address=old_primary_email,
                      to_email_address=new_primary_email)
            return super(EmailController, self).partial_update(request, *args, **kwargs) # pylint: disable=no-member
            # PyCQA/pylint issues #2854
        except EmailAddress.DoesNotExist:
            pass

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        email = instance.email
        if instance.primary:
            raise exceptions.ParseError('Cannot delete primary email')
        self.perform_destroy(instance)
        return response.Response({'deleted': email},
                                 status=status.HTTP_200_OK)


@decorators.api_view(['POST'])
def confirm_email(request, key):
    emailconfirmation = EmailConfirmationHMAC.from_key(key)
    if not emailconfirmation:
        raise exceptions.NotFound('email not found')
    emailconfirmation.confirm(request)
    return response.Response(
        {"detail": "Email is verified."},
        status=status.HTTP_200_OK)


@decorators.api_view(['POST'])
@decorators.permission_classes([IsOwner])
def resend_verification_email(request, email_id):
    try:
        email = EmailAddress.objects.get(id=email_id)
    except:
        raise exceptions.NotFound(
            'Email does not exist.') from EmailAddress.DoesNotExist
    email.send_confirmation(request)
    return response.Response(
        {"detail": "Verification email is sent."},
        status=status.HTTP_200_OK)
