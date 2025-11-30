from rest_framework import serializers
from api.models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email']  # Adjust fields as necessary

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()  # Nested serializer for author details

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date']  # Adjust fields as necessary

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author, created = Author.objects.get_or_create(**author_data)
        book = Book.objects.create(author=author, **validated_data)
        return book

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author')
        author, created = Author.objects.get_or_create(**author_data)
        instance.title = validated_data.get('title', instance.title)
        instance.author = author
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.save()
        return instance