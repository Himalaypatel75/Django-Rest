from django.contrib import admin
from .models import Blogs, BlogLikes

class BlogLikesAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog', 'user', 'like')

class BlogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_id', 'post_type', 'title', 'description', 'content', 'action_by', 'is_delete')

admin.site.register(BlogLikes, BlogLikesAdmin)
admin.site.register(Blogs, BlogsAdmin)
