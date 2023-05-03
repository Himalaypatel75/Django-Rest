from django.urls import path
from blog.views import BlogCreateAPIView, BlogListAPIView, BlogPrivateListAPIView, BlogRetrieveUpdateDestroyAPIView, UpdateOrCreateBlogLike

urlpatterns = [
    path('create', BlogCreateAPIView.as_view(), name='create-blog'),
    path('list', BlogListAPIView.as_view(), name='public-list-blog'),
    path('private-list', BlogPrivateListAPIView.as_view(), name='private-list-blog'),
    path('get-update-delete/<int:pk>', BlogRetrieveUpdateDestroyAPIView.as_view(), name='get-update-delete-blog'),
    
    path('like', UpdateOrCreateBlogLike.as_view(), name='like-create-or-update'),
    
]