from rest_framework import routers
from django.urls import path, include
from . import blog_views

router = routers.DefaultRouter()
router.register('blog', blog_views.BlogAPIView)
router.register('comment', blog_views.CommentAPIView)
router.register('reply', blog_views.ReplyAPIView)
router.register('issue', blog_views.IssueAPIView)
router.register('tooltip', blog_views.TooltipAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/reg/', include('dj_rest_auth.registration.urls'))
]
