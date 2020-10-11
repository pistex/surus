import json
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import response
from rest_framework import viewsets
from rest_framework import serializers
from apps.blog.models import (  # pylint: disable=import-error
    # pylint fails to locate apps created in subfolder
    Blog,
    Body,
    Comment,
    Reply,
    Issue,
    Tooltip,
    Image,
    Tag)
from apps.blog.serializers import (  # pylint: disable=import-error
    # pylint fails to locate apps created in subfolder
    BlogSerializer,
    CommentSerializer,
    ReplySerializer,
    IssueSerializer,
    TooltipSerializer,
    ImageSerializer)
from .permissions import IsCreator, IsAuthor, IsOwner, IsNotAnonymousObject

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

    # def get_permissions(self):
    #     if self.action == 'create':
    #         permission_classes = [IsCreator]
    #     elif self.action in update_destroy:
    #         permission_classes = [IsAuthor]
    #     else:
    #         permission_classes = [AllowAny]
    #     return [permission() for permission in permission_classes]

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    def retrieve(self, request, *args, **kwargs):  # pylint: disable=unused-argument # maintain overriding signature
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        history_data = Body.history.model.objects.filter(
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

# Anonymous comment cannot be edited, restriced in serializers.py


class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in update_destroy:
            permission_classes = [IsOwner | IsNotAnonymousObject]
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

    def get_permissions(self):
        if self.action in update_destroy:
            permission_classes = [IsOwner | IsNotAnonymousObject]
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
    queryset = Issue.objects.filter(is_public=True)
    serializer_class = IssueSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in update_destroy:
            permission_classes = [IsOwner]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class TooltipAPIView(viewsets.ModelViewSet):
    queryset = Tooltip.objects.all()
    serializer_class = TooltipSerializer

    def get_permissions(self):
        if self.action in create_update_destroy:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class ImageAPIView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    # def get_permissions(self):
    #     if self.action in create_update_destroy:
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [AllowAny]
    #     return [permission() for permission in permission_classes]

class TagAPIView(viewsets.ModelViewSet):
    class TagSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tag
            fields = '__all__'
            read_only_field = ['text']
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # def get_permissions(self):
    #     if self.action in create_update_destroy:
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [AllowAny]
    #     return [permission() for permission in permission_classes]
