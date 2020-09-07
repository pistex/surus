from django.db import models
# from django.utils.text import slugify
import django.contrib.auth
from simple_history.models import HistoricalRecords
# from simple_history.utils import update_change_reason

# Create your models here.
User = django.contrib.auth.get_user_model()
class Title(models.Model):
    en = models.CharField(max_length=100)
    th = models.CharField(max_length=100, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.en

class Body(models.Model):
    en = models.TextField()
    th = models.TextField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.en

class Tag(models.Model):
    en = models.CharField(max_length=16, unique=True)
    th = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.en

class Blog(models.Model):
    title = models.OneToOneField(Title, on_delete=models.RESTRICT)
    body = models.OneToOneField(Body, on_delete=models.RESTRICT)
    slug = models.SlugField(blank=True, unique=True)
    thumbmail = models.ImageField(default='default_thumbmail.png', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT)
    reason = models.CharField(max_length=100, blank=True)
    tag = models.ManyToManyField(Tag, blank=True, default=None)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id) + ": " + self.title.en

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print("Save model delete method is called.")
        super(Blog, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        print("Blog model delete method is called.")
        this_title = Title.objects.get(id=self.title.id)
        this_body = Body.objects.get(id=self.body.id)
        super(Blog, self).delete(using, keep_parents)
        this_title.delete()
        this_body.delete()

class Issue(models.Model):
    blog = models.ForeignKey(Blog, default=None, on_delete=models.SET_DEFAULT)
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.title

class Comment(models.Model):
    body = models.TextField(blank=False)
    blog = models.ForeignKey(Blog, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT)
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username + ": " + self.body + " in " + self.blog.title.en
class Reply(models.Model):
    body = models.TextField()
    comment = models.ForeignKey(Comment, default=None, on_delete=models.SET_DEFAULT)
    user = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT)
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username + ": " + self.body + " in " + self.comment.body


class Tooltip(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
