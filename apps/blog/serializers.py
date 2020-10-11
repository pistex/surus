from django.contrib import auth
from rest_framework import exceptions
from rest_framework import serializers
from .models import (
    Title,
    Body,
    Tag,
    Blog,
    Comment,
    Reply,
    Issue,
    Tooltip,
    Image)
User = auth.get_user_model()


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = [
            'en',
            'th'
            ]


class BodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Body
        fields = [
            'en',
            'th'
            ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['text']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
            ]


class BlogSerializer(serializers.ModelSerializer):
    title = TitleSerializer()
    body = BodySerializer()
    author = UserSerializer(read_only=True)
    tag = TagSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'

    # By default nested serializers are read-only.
    # If you want to support write-operations to a nested serializer field
    # you'll need to create create() and / or update() methods
    # in order to explicitly specify how the child relationships should be saved.
    # https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
    def create(self, validated_data):
        title_data = dict(validated_data.pop('title'))
        body_data = dict(validated_data.pop('body'))
        thumbnail = validated_data.pop('thumbnail')
        title = Title.objects.create(**title_data)
        body = Body.objects.create(**body_data)
        blog = Blog.objects.create(
            title=title,
            body=body,
            author=User.objects.get(id=self.context['request'].user.id),
            thumbnail=thumbnail)

        # Create tag
        tag_data = []
        for tag in validated_data.pop('tag'):
            tag_data.append(dict(tag))
        for tag in tag_data:
            if Tag.objects.filter(**tag).exists():
                tag = Tag.objects.filter(**tag)
                blog.tag.add(tag[0])
            else:
                tag = Tag.objects.create(**tag)
                blog.tag.add(tag)
        return blog
        # super(BlogSerializer, self).create(instance, validated_data)
        # return error repeatly becuase drf check if create method is overwritten here.

    def update(self, instance, validated_data):
        # update title
        if 'title' in validated_data:
            title_data = dict(validated_data.pop('title'))
            title = Title.objects.filter(id=instance.title.id)
            title.update(**title_data)
            title[0].save()
            instance = Blog.objects.get(id=instance.id)

        # update body
        if 'body' in validated_data:
            body_data = dict(validated_data.pop('body'))
            body = Body.objects.filter(id=instance.body.id)
            body.update(**body_data)
            body[0].save()
            instance = Blog.objects.get(id=instance.id)

        # update tag
        if 'tag' in validated_data:
            instance.tag.clear()
            tag_data = []
            for tag in validated_data.pop('tag'):
                tag_data.append(dict(tag))
            for tag in tag_data:
                if Tag.objects.filter(**tag).exists():
                    tag = Tag.objects.filter(**tag)
                    instance.tag.add(tag[0])
                else:
                    tag = Tag.objects.create(**tag)
                    instance.tag.add(tag)
        return super(BlogSerializer, self).update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class BlogIdTitle(BlogSerializer):
        class Meta:
            model = Blog
            fields = ['id', 'title']
    blog = BlogIdTitle(read_only=True)

    class UserIdUsername(UserSerializer):
        class Meta:
            model = User
            fields = ['id', 'username']
    user = UserIdUsername(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    # By default nested serializers are read-only.
    # If you want to support write-operations to a nested serializer field
    # you'll need to create create() and / or update() methods
    # in order to explicitly specify how the child relationships should be saved.
    # https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
    def create(self, validated_data):
        try:
            blog_id = self.context['request'].data["blog_id"]
        except:
            raise exceptions.ParseError("No blog_id provied") from KeyError
        if not isinstance(blog_id, int):
            raise exceptions.ParseError(
                "blog_id should be input as an integer.") from TypeError
        try:
            blog = Blog.objects.get(id=self.context['request'].data['blog_id'])
        except:
            raise exceptions.NotFound(
                'The blog with given id does not exist.') from Blog.DoesNotExist
        
        # Allow guest comment.
        if self.context['request'].user.is_authenticated:
            user = User.objects.get(id=self.context['request'].user.id)
        else:
            user = None
        comment = Comment.objects.create(
            blog=blog,
            user=user,
            **validated_data)
        return comment

    def update(self, instance, validated_data):
        if instance.user is None:
            raise exceptions.PermissionDenied('This comment cannot be modified')
        return super().update(instance, validated_data)


class ReplySerializer(serializers.ModelSerializer):
    class CommentIdBodyBlog(CommentSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'body',
                'blog'
                ]
    comment = CommentIdBodyBlog(read_only=True)

    class UserIdUsername(UserSerializer):
        class Meta:
            model = User
            fields = [
                'id',
                'username'
                ]
    user = UserIdUsername(read_only=True)

    class Meta:
        model = Reply
        fields = '__all__'

    def create(self, validated_data):
        try:
            comment_id = self.context['request'].data["comment_id"]
        except:
            raise exceptions.ParseError("No comment_id provied") from KeyError
        if not isinstance(comment_id, int):
            raise exceptions.ParseError(
                "comment_id should be input as an integer.") from TypeError
        comment = Comment.objects.get(
            id=self.context['request'].data['comment_id'])
        if self.context['request'].user.is_authenticated:
            user = User.objects.get(id=self.context['request'].user.id)
        else:
            user = None
        reply = Reply.objects.create(
            comment=comment,
            user=user,
            **validated_data)
        return reply

    def update(self, instance, validated_data):
        if instance.user is None:
            raise exceptions.PermissionDenied(
                'This reply cannot be modified')
        return super().update(instance, validated_data)


class IssueSerializer(serializers.ModelSerializer):
    class BlogIdTitle(BlogSerializer):
        class Meta:
            model = Blog
            fields = [
                'id',
                'title'
                ]
    blog = BlogIdTitle(read_only=True)

    class UserIdUsername(UserSerializer):
        class Meta:
            model = User
            fields = ['id', 'username']
    user = UserIdUsername(read_only=True)

    class Meta:
        model = Issue
        fields = [
            'title',
            'body',
            'blog',
            'user',
            'category',
            'is_public',
            'is_solved'
            ]

    def create(self, validated_data):
        try:
            blog_id = self.context['request'].data["blog_id"]
        except:
            raise exceptions.ParseError("No blog_id provied") from KeyError
        if not isinstance(blog_id, int):
            raise exceptions.ParseError(
                "blog_id should be input as an integer.") from TypeError

        blog = Blog.objects.get(id=self.context['request'].data['blog_id'])
        if self.context['request'].user.is_authenticated:
            user = User.objects.get(id=self.context['request'].user.id)
        else:
            user = None
        issue = Issue.objects.create(
            blog=blog,
            user=user,
            **validated_data)
        issue.is_public = False
        issue.is_solved = False
        issue.save()
        return issue

    def update(self, instance, validated_data):
        if instance.is_public:
            raise exceptions.PermissionDenied(
                'Public issue is not editable.')
        return super().update(instance, validated_data)


class TooltipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tooltip
        fields ='__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
