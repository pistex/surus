from allauth.account.utils import sync_user_email_addresses
from django.contrib import auth
from allauth.account.models import EmailAddress
from allauth.account import signals
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import mixins
from rest_framework import response
from rest_framework import exceptions
from rest_framework import status
from rest_framework import decorators
from .permissions import IsUser
User = auth.get_user_model()
create_update_destroy = ['create', 'update', 'partial_update', 'destroy']


class ProfileController(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'profile_picture', 'username',
                      'first_name', 'last_name', 'date_joined', 'last_login')
            read_only_fields = ('id', 'date_joined', 'last_login')
    queryset = User.objects.all()
    serializer_class = Serializer
    # permission_classes = [IsUser]


class EmailController(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = EmailAddress
            fields = ('id', 'email', 'primary', 'verified')
            read_only_fields = ('email', 'primary', 'verified')
    queryset = EmailAddress.objects.all()
    serializer_class = Serializer
    # permission_classes = [IsOwner]
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise exceptions.MethodNotAllowed(
                "method PUT is not allow for this endpoint.")
        requested_user = self.initialize_request(request, *args, **kwargs).user
        sync_user_email_addresses(requested_user)
        return super(EmailController, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        signals.email_added.send(sender=self.request.user.__class__,
                                 request=self.request,
                                 user=self.request.user,
                                 email_address=request.data.email)
        return super(EmailController, self).create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if "verified" in request.data:
            raise exceptions.ParseError('Cannot change verification status on this endpint.')
        if "email" in request.data:
            raise exceptions.ParseError('Cannot change email address on this endpint.')
        if not request.data['primary']:
            raise exceptions.ParseError('This endpoint is for making primary email only')
        try:
            new_primary_email = EmailAddress.objects.get(id=request.data['id'])
            if not new_primary_email.verified \
                and EmailAddress.objects.filter(user=request.user, verified=True).exists():
                raise exceptions.ParseError(
                    'Please verify your email before make it primary')
            try:
                old_primary_email = EmailAddress.objects \
                    .get(user=request.user, primary=True)
            except EmailAddress.DoesNotExist:
                old_primary_email = None
            if new_primary_email == old_primary_email:
                return response.Response({"detail": ("The email is already primary.")}, status=status.HTTP_200_OK)
            new_primary_email.set_as_primary()
            signals.email_changed \
                .send(sender=request.user.__class__,
                      request=request,
                      user=request.user,
                      from_email_address=old_primary_email,
                      to_email_address=new_primary_email)
            return super(EmailController, self).partial_update(request, *args, **kwargs)
        except EmailAddress.DoesNotExist:
            pass

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.primary:
            raise exceptions.ParseError('Cannot delete primary email')
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


@decorators.api_view(['POST'])
def resend_verification_email(request, email_id):
    try:
        email = EmailAddress.objects.get(id=email_id)
    except:
        raise exceptions.NotFound(
            'Email does not exist.') from EmailAddress.DoesNotExist
    email.send_confirmation(request)
    return response.Response({"detail": ("Verification email is sent.")}, status=status.HTTP_200_OK)
