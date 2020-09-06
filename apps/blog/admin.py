from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Title, Body, Blog
# Register your models here.
admin.site.register(Title, SimpleHistoryAdmin)
admin.site.register(Body, SimpleHistoryAdmin)
admin.site.register(Blog, SimpleHistoryAdmin)
