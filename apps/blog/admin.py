from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Title, Body, Tag, Blog, Comment
# Register your models here.
admin.site.register(Title, SimpleHistoryAdmin)
admin.site.register(Body, SimpleHistoryAdmin)
admin.site.register(Tag)
admin.site.register(Blog, SimpleHistoryAdmin)
admin.site.register(Comment, SimpleHistoryAdmin)
