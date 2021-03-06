import json
import django_filters.rest_framework
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import response
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework import status
from apps.blog.models import (  # pylint: disable=import-error
    # pylint fails to locate apps created in subfolder
    Blog,
    Body,
    Comment,
    Reply,
    Issue,
    Image,
    Tag)
from apps.blog.serializers import (  # pylint: disable=import-error
    # pylint fails to locate apps created in subfolder
    BlogSerializer,
    CommentSerializer,
    ReplySerializer,
    IssueSerializer,
    ImageSerializer)
from .permissions import IsCreator, IsAuthor, IsOwner, IsNotAnonymousObjectOrPerformByAdminOnly, IsAdminUser

create_update_destroy = [
    'create',
    'update',
    'partial_update',
    'destroy'
]
update_destroy = [
    'update',
    'partial_update',
    'destroy'
]

class BlogAPIView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filterset_fields = ['slug']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminUser | IsCreator]
        elif self.action in update_destroy:
            permission_classes = [IsAdminUser | IsAuthor]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):  # pylint: disable=unused-argument # maintain overriding signature
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        history_data = Body.history.model.objects.filter(
            id=instance.body.id)
        json_history = '{'
        for history in history_data.values():
            history.update(
                {'history_date': history['history_date'].strftime('%Y-%m-%d %H:%M:%S')})
            json_history += '"' \
                + history['history_date'] \
                + '": ' + json.dumps(history) \
                + ', '
        json_history = json_history[:-2] + '}'
        json_data = json.dumps(serializer.data)[:-1] \
            + ', "history": ' \
            + json_history \
            + '}'
        return response.Response(json.loads(json_data))


class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_fields = ['blog']

    def get_permissions(self):
        if self.action in update_destroy:
            permission_classes = [
                IsOwner | IsNotAnonymousObjectOrPerformByAdminOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):  # pylint: disable=unused-argument # maintain overriding signature
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        history_data = Comment.history.model.objects.filter(
            id=serializer.data["id"])
        json_history = '{'
        for history in history_data.values():
            history.update(
                {'history_date': history['history_date'].strftime('%Y-%m-%d %H:%M:%S')})
            json_history += '"' \
                + history['history_date'] \
                + '": ' + json.dumps(history) \
                + ', '
        json_history = json_history[:-2] + '}'
        json_data = json.dumps(serializer.data)[:-1] \
            + ', "history": ' \
            + json_history \
            + '}'
        return response.Response(json.loads(json_data))


class ReplyAPIView(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    filterset_fields = ['comment']

    def get_permissions(self):
        if self.action in update_destroy:
            permission_classes = [
                IsOwner | IsNotAnonymousObjectOrPerformByAdminOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):  # pylint: disable=unused-argument # maintain overriding signature
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        history_data = Reply.history.model.objects.filter(
            id=serializer.data["id"])
        json_history = '{'
        for history in history_data.values():
            history.update(
                {'history_date': history['history_date'].strftime('%Y-%m-%d %H:%M:%S')})
            json_history += '"' \
                + history['history_date'] \
                + '": ' \
                + json.dumps(history) \
                + ', '
        json_history = json_history[:-2] + '}'
        json_data = json.dumps(serializer.data)[:-1] \
            + ', "history": ' \
            + json_history \
            + '}'
        return response.Response(json.loads(json_data))


class IssueAPIView(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_permissions(self):
        if self.action in update_destroy:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class ImageAPIView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_permissions(self):
        if self.action in create_update_destroy:
            permission_classes = [IsAdminUser | IsCreator]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.caption == 'default_thumbnail':
            raise exceptions.ParseError('Default thumbnail cannot belete.')
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class TagAPIView(viewsets.ModelViewSet):
    class TagSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tag
            fields = '__all__'
            read_only_field = ['text']
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action in create_update_destroy:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
