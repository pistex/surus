from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register('blog', views.BlogAPIView)
router.register('comment', views.CommentAPIView)
router.register('reply', views.ReplyAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('debugging/', views.debugging)
]
