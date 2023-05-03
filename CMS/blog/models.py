from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
# Create your models here.

def increment_blog_number():
    last_blog = Blogs.objects.last()
    if not last_blog:
        return '1000'
    post_no = last_blog.post_id
    post_int = int(post_no)
    new_post_int = post_int + 1
    new_post_no = str(new_post_int)
    return new_post_no

post_type = [
    ('public','public'),
    ('private','private'),
]

class Blogs(BaseModel):
    post_id = models.CharField(max_length=150, default=increment_blog_number)
    post_type = models.CharField(choices=post_type, max_length=150, default="public")
    title = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    action_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, db_index=True)
    is_delete = models.BooleanField(default=False)
    
class BlogLikes(BaseModel):
    blog = models.ForeignKey(Blogs, null=True, on_delete=models.CASCADE, db_index=True, related_name="user_likes")
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, db_index=True)
    like = models.BooleanField(default=True)