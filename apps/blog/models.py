from django.db import models
from django.utils.text import slugify
from apps.user.models import User
from simple_history.models import HistoricalRecords
from simple_history.utils import update_change_reason

# Create your models here.


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
    en = models.CharField(max_length=16)
    th = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.en
    
class Blog(models.Model):
    title = models.OneToOneField(Title, on_delete=models.RESTRICT)
    body = models.OneToOneField(Body, on_delete=models.RESTRICT)
    slug = models.SlugField(blank=True, editable=False, unique=True)
    thumbmail = models.ImageField(default='default_thumbmail.png', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT)
    reason = models.CharField(max_length=100, blank=True)
    tag = models.ManyToManyField(Tag)
    history = HistoricalRecords()

    def __str__(self):
        return self.title.en

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title.en)
        if self.pk == None:
            self.reason = "created"
        if self.pk != None and self.reason == ("created" or "no change reason"):
            self.reason = "no change reason"
        super().save(*args, **kwargs)
        update_change_reason(self, self.reason)
    
    def delete(self, *args, **kwargs):
        this_title = Title.objects.get(id=self.title.id)
        this_body = Body.objects.get(id=self.body.id)
        super().delete(*args, **kwargs)
        this_title.delete()
        this_body.delete()
