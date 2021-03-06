from rest_framework import routers
from django.urls import path, include, re_path
from . import blog_views
from . import admin_views
from . import profile_views
from . import social_login_views

# Public pages
router = routers.DefaultRouter()
router.register('blog', blog_views.BlogAPIView)
router.register('comment', blog_views.CommentAPIView)
router.register('reply', blog_views.ReplyAPIView)
router.register('issue', blog_views.IssueAPIView)
router.register('image', blog_views.ImageAPIView)
router.register('tag', blog_views.TagAPIView)

# Admin panel
router.register('rest_admin/group', admin_views.GroupModelController)

# User Profile
router.register('user_profile', profile_views.ProfileController)
router.register('user_email', profile_views.EmailController)

urlpatterns = [
    # Public pages
    path('', include(router.urls)),

    # Admin panel
    path('rest_admin/all_user/', admin_views.all_user),
    path('rest_admin/delete_user/', admin_views.delete_user),
    path('rest_admin/user/<int:user_id>/', admin_views.user_detail),
    path('rest_admin/user/<int:user_id>/update_groups/',
         admin_views.update_user_groups),

    # Social Login
    path('authentication/facebook/',
         social_login_views.FacebookLogin.as_view(),
         name='facebook_login'),
    path('authentication/google/',
         social_login_views.GoogleLogin.as_view(),
         name='google_login'),
    path('authentication/facebook/connect/',
         social_login_views.FacebookConnect.as_view(),
         name='facebook_connect'),
    path('authentication/google/connect/',
         social_login_views.GoogleConnect.as_view(),
         name='google_connect'),
    # User profile
    path('authentication/password/initialize/',
          profile_views.initialize_password)
]
