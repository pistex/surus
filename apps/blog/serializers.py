from django.contrib import auth
from rest_framework import exceptions
from rest_framework import serializers
from .models import Title, Body, Tag, Blog, Comment, Reply
User = auth.get_user_model()


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ['en', 'th']

class BodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Body
        fields = ['en', 'th']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['en', 'th']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class BlogSerializer(serializers.ModelSerializer):
    title = TitleSerializer()
    body = BodySerializer()
    author = UserSerializer(read_only=True)
    tag = TagSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'
        extra_kwargs = {'tag': {'required': False}}

    def create(self, validated_data):
        if not self.context['request'].user.is_authenticated:
            raise exceptions.AuthenticationFailed('No user authenticated')
        title_data = dict(validated_data.pop('title'))
        body_data = dict(validated_data.pop('body'))
        title = Title.objects.create(**title_data)
        body = Body.objects.create(**body_data)
        blog = Blog.objects.create(
            title=title,
            body=body,
            author=User.objects.get(id=self.context['request'].user.id))

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
        # super(BlogSerializer, self).create(instance, validated_data) return error repeatly.

    def update(self, instance, validated_data):
        if not self.context['request'].user.is_authenticated:
            raise exceptions.AuthenticationFailed('No user authenticated')
        if self.context['request'].user.id != instance.author.id:
            raise exceptions.PermissionDenied(
                'You don\'t have permission to modify this post.')

        # update title
        if 'title' in validated_data:
            title_data = dict(validated_data.pop('title'))
            title = Title.objects.filter(id=instance.title.id)
            title.update(**title_data)
            Blog.objects.get(id=instance.id)
            # A model instance will not update one to one field
            # ultil it being call agian.

        # update body
        if 'body' in validated_data:
            body_data = dict(validated_data.pop('body'))
            body = Title.objects.filter(id=instance.body.id)
            body.update(**body_data)
            Blog.objects.get(id=instance.id)
            # A model instance will not update one to one field
            # ultil it being call agian.

        # update tag
        instance.tag.clear()
        if 'tag' in validated_data:
            tag_data = []
            for tag in validated_data.pop('tag'):
                tag_data.append(dict(tag))
            for tag in tag_data:
                if Tag.objects.filter(**tag).exists():
                    tag = Tag.objects.filter(**tag)
                    instance.tag.add(tag[0])
                    instance.save()
                else:
                    tag = Tag.objects.create(**tag)
                    instance.tag.add(tag)
                    instance.save()
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

    def create(self, validated_data):
        if not "blog_id" in self.context['request'].data:
            raise exceptions.ParseError("No blog_id provied")
        if not self.context['request'].data["blog_id"].isnumeric():
            raise exceptions.ParseError("Invalid blog_id")
        blog = Blog.objects.get(id=self.context['request'].data['blog_id'])
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
            raise exceptions.PermissionDenied('This reply cannot be modified')
        if self.context['request'].user.id != instance.user.id:
            raise exceptions.PermissionDenied(
                'You don\'t have permission to modify this reply.')
        return super().update(instance, validated_data)


class ReplySerializer(serializers.ModelSerializer):
    class CommentIdBodyBlog(CommentSerializer):
        class Meta:
            model = Comment
            fields = ['id', 'body', 'blog']
    comment = CommentIdBodyBlog(read_only=True)

    class UserIdUsername(UserSerializer):
        class Meta:
            model = User
            fields = ['id', 'username']
    user = UserIdUsername(read_only=True)

    class Meta:
        model = Reply
        fields = '__all__'

    def create(self, validated_data):
        if not "comment_id" in self.context['request'].data:
            raise exceptions.ParseError("No comment_id provied")
        if not self.context['request'].data["comment_id"].isnumeric():
            raise exceptions.ParseError("Invalid comment_id")
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
                'This comment cannot be modified')
        if self.context['request'].user.id != instance.user.id:
            raise exceptions.PermissionDenied(
                'You don\'t have permission to modify this comment.')
        return super().update(instance, validated_data)
