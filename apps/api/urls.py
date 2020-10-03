from rest_framework import routers
from django.urls import path, include
from . import blog_views
from . import admin_views
from . import profile_views

# Public pages
router = routers.DefaultRouter()
router.register('blog', blog_views.BlogAPIView)
router.register('comment', blog_views.CommentAPIView)
router.register('reply', blog_views.ReplyAPIView)
router.register('issue', blog_views.IssueAPIView)
router.register('tooltip', blog_views.TooltipAPIView)

# Admin panel
router.register('rest_admin/group', admin_views.GroupModelController)

#User Profile
router.register('profile', profile_views.ProfileController)

urlpatterns = [
    # Public pages
    path('', include(router.urls)),

    # Admin panel
    path('rest_admin', admin_views.hello_world),
    path('rest_admin/all_user/', admin_views.all_user),
    path('rest_admin/delete_user/', admin_views.delete_user),
    path('rest_admin/user/<int:user_id>', admin_views.user_detail),
    path('rest_admin/user/<int:user_id>/update_groups',
         admin_views.update_user_groups)
]
