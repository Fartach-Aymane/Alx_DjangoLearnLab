from rest_framework import serializers
from .models import Post, Comment, Like
from django.contrib.auth import get_user_model

User = get_user_model()

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # Display the username, read-only
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'like_count', 'comment_count']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_comment_count(self, obj):
        return obj.comments.count()
         
# Comments serializer
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # Display the username, read-only
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

# Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']