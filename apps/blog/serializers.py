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
    tag = TagSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'

    def create(self, validated_data):
        if not self.context['request'].user.is_authenticated:
            raise exceptions.AuthenticationFailed('No user authenticated')
        title_data = dict(validated_data.pop('title'))
        body_data = dict(validated_data.pop('body'))
        tag_data = []
        for tag in validated_data.pop('tag'):
            tag_data.append(dict(tag))
        title = Title.objects.create(**title_data)
        body = Body.objects.create(**body_data)
        blog = Blog.objects.create(
            title=title, body=body, author=User.objects.get(id=self.context['request'].user.id), **validated_data)
        for tag in tag_data:
            if Tag.objects.filter(**tag).exists():
                tag = Tag.objects.filter(**tag)
                blog.tag.add(tag[0])
            else:
                tag = Tag.objects.create(**tag)
                blog.tag.add(tag)
        return blog
