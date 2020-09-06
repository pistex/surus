import pprint
from django.http import HttpResponse
from rest_framework import viewsets
from apps.blog.models import Blog
from apps.blog.serializers import BlogSerializer

def debugging(request):
    """Function based view for debugging"""
    pprint.pprint(request.META)
    return HttpResponse("None")


class BlogAPIView(viewsets.ModelViewSet):
    """Control access permission dor SalesData"""
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
