from django.db import models
from django.contrib import auth
from django.utils.text import slugify
from simple_history.models import HistoricalRecords
from simple_history.utils import update_change_reason

User = auth.get_user_model()


class Image(models.Model):
    image = models.ImageField(upload_to='blog')
    caption = models.CharField(max_length=200, blank=True)

    def delete(self, *arg, **kwarg):
        # todo implement file changed
        self.image.storage.delete(self.image.name)
        super(Image, self).delete(*arg, **kwarg)


def get_default_thumbnail():
    return Image.objects.get(caption='default_thumbnail')


class Title(models.Model):
    en = models.CharField(max_length=200)
    th = models.CharField(max_length=200, blank=True)
    history = HistoricalRecords(cascade_delete_history=True)

    def __str__(self):
        return self.en


class Body(models.Model):
    en = models.TextField()
    th = models.TextField(blank=True)
    history = HistoricalRecords(cascade_delete_history=True)

    def __str__(self):
        return self.en


class Tag(models.Model):
    text = models.CharField(max_length=16, blank=False)

    def __str__(self):
        return self.text


class Blog(models.Model):
    """
    I found a limit of DRF here. The problem is DRF cannot parse array field
    (ManyToManyField) uploaded from 'multipart/form-data'.
    At least not by default. The only way available is to use JSON.
    And anothor problem come up because a blob cannot be sent by JSON.
    So I end up use ForeignKey for thumbnail.
    """
    title = models.OneToOneField(Title, on_delete=models.RESTRICT)
    body = models.OneToOneField(Body, on_delete=models.RESTRICT)
    slug = models.SlugField(blank=True, unique=True, max_length=255)

    thumbnail = models.ForeignKey(
        Image,
        default=1,
        on_delete=models.SET(get_default_thumbnail),
        null=True)
    author = models.ForeignKey(
        User,
        default=None,
        on_delete=models.SET_DEFAULT,
        null=True)
    reason = models.CharField(max_length=100, blank=True)
    tag = models.ManyToManyField(Tag, blank=True, default=None)
    is_featured = models.BooleanField(default=False)
    history = HistoricalRecords(cascade_delete_history=True)

    def __str__(self):
        return str(self.id) + ': ' + self.title.en

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None):
        if self.title:
            self.slug = slugify(self.title.en)
        if self.id is None and not self.thumbnail:
            self.thumbnail = get_default_thumbnail()
        if self.id is None:
            self.reason = 'created'
        if self.id is not None:
            if self.reason == ('created' or 'no change reason' or '' or None):
                self.reason = 'no change reason'
        super(Blog, self).save(
            force_insert,
            force_update,
            using,
            update_fields)
        update_change_reason(self, self.reason)
        update_change_reason(self.title, self.reason)
        update_change_reason(self.body, self.reason)

    def delete(self, using=None, keep_parents=False):
        this_title = Title.objects.get(id=self.title.id)
        this_body = Body.objects.get(id=self.body.id)
        super(Blog, self).delete(using, keep_parents)
        this_title.delete()
        this_body.delete()


class Comment(models.Model):
    body = models.TextField(blank=False)
    blog = models.ForeignKey(Blog, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, default=None, null=True, on_delete=models.SET_DEFAULT)
    reason = models.CharField(max_length=100, blank=True)
    history = HistoricalRecords(cascade_delete_history=True)

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None):
        if self.id is None:
            self.reason = 'created'
        if self.id is not None:
            if self.reason == ('created' or 'no change reason' or ''):
                self.reason = 'no change reason'
        super(Comment, self).save(
            force_insert,
            force_update,
            using,
            update_fields)
        update_change_reason(self, self.reason)

    def __str__(self):
        return (self.user.username if bool(self.user) else 'Anonymous')\
            + ': ' + self.body\
            + ' in ' + self.blog.title.en


class Reply(models.Model):
    body = models.TextField()
    comment = models.ForeignKey(
        Comment, default=None, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, default=None, null=True, on_delete=models.SET_DEFAULT)
    reason = models.CharField(max_length=100, blank=True)
    history = HistoricalRecords(cascade_delete_history=True)

    def __str__(self):
        return (self.user.username if bool(self.user) else 'Anonymous')\
            + ': ' + self.body\
            + ' in ' + self.comment.body

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None):
        if self.id is None:
            self.reason = 'created'
        if self.id is not None:
            if self.reason == ('created' or 'no change reason' or ''):
                self.reason = 'no change reason'
        super(Reply, self).save(
            force_insert,
            force_update,
            using,
            update_fields)
        update_change_reason(self, self.reason)


class Issue(models.Model):
    ISSUE_CATEGORY_CHOICE = [
        ('CODE', 'Code'),
        ('SYSTEM', 'System'),
        ('TYPO', 'Typo'),
        ('ETC', 'Etc')
    ]
    title = models.CharField(max_length=200)
    body = models.TextField()
    blog = models.ForeignKey(
        Blog, default=None, null=True, on_delete=models.SET_DEFAULT)
    user = models.ForeignKey(
        User, default=None, null=True, on_delete=models.SET_DEFAULT)
    category = models.CharField(
        max_length=10, blank=False, choices=ISSUE_CATEGORY_CHOICE, default='ETC')
    is_solved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
