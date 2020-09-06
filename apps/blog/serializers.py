from rest_framework import serializers
from .models import Title, Body, Tag, Blog
from apps.user.models import User
from rest_framework import exceptions


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
    tag = TagSerializer(required=False, many=True)

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
            author=User.objects.get(id=self.context['request'].user.id),
            **validated_data)

        # Create track
        if 'tag' in validated_data:
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

    def update(self, instance, validated_data):
        if not self.context['request'].user.is_authenticated:
            raise exceptions.AuthenticationFailed('No user authenticated')
        if self.context['request'].user.id != instance.author.id:
            raise exceptions.AuthenticationFailed('You don\'t have permission to edit this post.')
        blog = Blog.objects.filter(id=instance.id)
        # update title
        if 'title' in validated_data:
            title_data = dict(validated_data.pop('title'))
            title = Title.objects.filter(id=instance.title.id)
            title.update(**title_data)
        #update body
        if 'body' in validated_data:
            body_data = dict(validated_data.pop('body'))
            body = Title.objects.filter(id=instance.body.id)
            body.update(**title_data)
        instance.tag.clear()
        if 'tag' in validated_data:
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
        blog.update(
            author=User.objects.get(id=self.context['request'].user.id),
            **validated_data)
        instance.save()
        return instance
