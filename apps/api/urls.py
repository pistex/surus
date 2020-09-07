from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register('blog', views.BlogAPIView)
router.register('comment', views.CommentAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('debugging/', views.debugging)
]
