import pprint
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import viewsets
from apps.blog.models import (  # pylint: disable=import-error
    # pylint fails to locate apps created in subfolder
    Blog,
    Body,
    Comment,
    Reply,
    Issue,
    Tooltip)
from apps.blog.serializers import ( # pylint: disable=import-error
    # pylint fails to locate apps created in subfolder
    BlogSerializer,
    CommentSerializer,
    ReplySerializer,
    IssueSerializer,
    TooltipSerializer)


@csrf_exempt
def debugging(request):
    """Declare function based view for debugging."""
    pprint.pprint(request.POST)
    return HttpResponse("None")


class BlogAPIView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def retrieve(self, request, *args, **kwargs):  # pylint: disable=unused-argument # maintain overriding signature
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        history_data = Body.history.model.objects.filter(id=serializer.data["id"])
        json_history = '{'
        for history in history_data.values():
            history.update(
                {'history_date': history['history_date'].strftime('%Y-%m-%d %H:%M:%S')})
            json_history += '"' + history['history_date'] + '": ' + json.dumps(history) + ', '
        json_history = json_history[:-2] + '}'
        json_data = json.dumps(serializer.data)[:-1] + ', "history": ' + json_history + '}'
        return Response(json.loads(json_data))

class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def retrieve(self, request, *args, **kwargs):  # pylint: disable=unused-argument # maintain overriding signature
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        history_data = Comment.history.model.objects.filter(
            id=serializer.data["id"])
        json_history = '{'
        for history in history_data.values():
            history.update(
                {'history_date': history['history_date'].strftime('%Y-%m-%d %H:%M:%S')})
            json_history += '"' + \
                history['history_date'] + '": ' + json.dumps(history) + ', '
        json_history = json_history[:-2] + '}'
        json_data = json.dumps(serializer.data)[
            :-1] + ', "history": ' + json_history + '}'
        return Response(json.loads(json_data))

class ReplyAPIView(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def retrieve(self, request, *args, **kwargs):  # pylint: disable=unused-argument # maintain overriding signature
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        history_data = Comment.history.model.objects.filter(
            id=serializer.data["id"])
        json_history = '{'
        for history in history_data.values():
            history.update(
                {'history_date': history['history_date'].strftime('%Y-%m-%d %H:%M:%S')})
            json_history += '"' + \
                history['history_date'] + '": ' + json.dumps(history) + ', '
        json_history = json_history[:-2] + '}'
        json_data = json.dumps(serializer.data)[
            :-1] + ', "history": ' + json_history + '}'
        return Response(json.loads(json_data))

class IssueAPIView(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class TooltipAPIView(viewsets.ModelViewSet):
    queryset = Tooltip.objects.all()
    serializer_class = TooltipSerializer
