from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from blog.serializer import BlogSerializer, BlogLikesSerializer, BlogViewSerializer
from .models import BlogLikes, Blogs
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Count, Q
from django.db.models import Prefetch


class BlogCreateAPIView(CreateAPIView):
    queryset = Blogs.objects.all()
    serializer_class = BlogSerializer
    
    def perform_create(self, serializer):
        serializer.save(action_by = self.request.user)
        
        
class BlogListAPIView(ListAPIView):
    serializer_class = BlogViewSerializer
    
    def get_queryset(self):
        queryset = Blogs.objects.filter(is_delete = False, post_type = "public").annotate(
        like_count=Count('user_likes', filter=Q(user_likes__like=True))
        ).prefetch_related(
            Prefetch(
            'user_likes',
            queryset=BlogLikes.objects.filter(like=True)
            )
        )
        return queryset 
        
        
class BlogPrivateListAPIView(ListAPIView):
    serializer_class = BlogViewSerializer
    
    def get_queryset(self):
        queryset = Blogs.objects.filter(is_delete = False, action_by = self.request.user, post_type = "private").annotate(
        like_count=Count('user_likes', filter=Q(user_likes__like=True))
        ).prefetch_related(
            Prefetch(
            'user_likes',
            queryset=BlogLikes.objects.filter(like=True)
            )
        )
        return queryset 
    
        
class BlogRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "delete", "patch"]
    queryset = Blogs.objects.all().select_related('action_by').annotate(
        like_count=Count('user_likes', filter=Q(user_likes__like=True))
        ).prefetch_related(
            Prefetch(
            'user_likes',
            queryset=BlogLikes.objects.filter(like=True)
            )
        )
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        kwargs['partial'] = True
        if instance.action_by.id == self.request.user.id:
            return self.update(request, *args, **kwargs)
        else:
            return Response({"error": "You are not authorized to perform this action."}, status=status.HTTP_401_UNAUTHORIZED)
        
    def perform_destroy(self, instance):
        instance = self.get_object()
        if instance.action_by.id == self.request.user.id:
            instance.is_delete = True
            instance.save()
        else:
            instance.is_delete = False
            instance.save()
            
        
    def get_serializer_class(self):
        type = self.request.method
        if type == "GET":
            return BlogViewSerializer
        else:
            return BlogSerializer
        
class UpdateOrCreateBlogLike(APIView):
    
    def post(self, request):
        serializer = BlogLikesSerializer(data=request.data)
        if serializer.is_valid():
            # Check if a BlogLikes instance with the same blog and user already exists
            obj, created = BlogLikes.objects.update_or_create(
                blog=serializer.validated_data['blog'],
                user=self.request.user,
                defaults={'like': serializer.validated_data['like']}
            )
            return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)