from rest_framework.serializers import ModelSerializer
from user.serializer import UserSignUpSerializer
from blog.models import Blogs, BlogLikes
from rest_framework import serializers


class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blogs
        fields = ('id','title','description','content','action_by','is_delete','post_type')
        read_only_fields = ['id']
      
      
class BlogLikesSerializer(ModelSerializer):
    class Meta:
        model = BlogLikes
        fields = ('id','blog','user','like')
        read_only_fields = ['id']
        
        
class BlogViewSerializer(ModelSerializer):
    action_by = UserSignUpSerializer()
    count = serializers.IntegerField(source = "bloglikes")
    users_likes = BlogLikesSerializer(source = "user_likes", many=True)
    
    class Meta:
        model = Blogs
        fields = ('id','title','description','content','action_by','is_delete','count','post_type','users_likes')
        read_only_fields = fields
        
