import pprint
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from apps.blog.models import Blog, Comment, Reply
from apps.blog.serializers import BlogSerializer, CommentSerializer, ReplySerializer


@csrf_exempt
def debugging(request):
    """Function based view for debugging"""
    pprint.pprint(request.POST)
    return HttpResponse("None")


class BlogAPIView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ReplyAPIView(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
