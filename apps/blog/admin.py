"""
apps.blog.admin.py is used for configure django-admin dashboard (Default = locahost:8000/admin)
"""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Title, Body, Tag, Blog, Comment

admin.site.register(Title, SimpleHistoryAdmin)
admin.site.register(Body, SimpleHistoryAdmin)
admin.site.register(Tag)
admin.site.register(Blog, SimpleHistoryAdmin)
admin.site.register(Comment, SimpleHistoryAdmin)
