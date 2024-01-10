from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from account.utils import *

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=128, db_index=True, null=True)
    draft = models.BooleanField(default=True)

    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'blog'


class Reply(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name='replies', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        app_label = 'blog'
        verbose_name_plural = 'Replies'



class Professor(models.Model):
    name = models.CharField(max_length=1000,null=True, blank=True)
    title = models.CharField(max_length=1000, null=True,blank=True)
    phone = models.CharField(max_length=1000, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    achievements = models.TextField(null=True,blank=True)
    # school = models.CharField(max_length=1000,null=True,blank=True)
    # college = models.CharField(max_length=1000,null=True,blank=True)
    city = models.CharField(max_length=1000,null=True,blank=True)
    province = models.CharField(max_length=1000,null=True,blank=True)
    country = models.CharField(max_length=1000,null=True,blank=True)
    email = models.EmailField(null=True, blank=True,unique=True)
    slug = models.SlugField(unique=True,null=True)
    image_url = models.URLField(null=True, blank=True)
    research_areas = models.TextField(null=True,blank=True)
    university = models.CharField(max_length=1000,null=True,blank=True)
    department = models.CharField(max_length=1000,null=True,blank=True)



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug_shortcode(size=20, model_=Professor)
        return super(Professor, self).save(*args,**kwargs)



    class Meta:
        unique_together = ['name', 'title','research_areas','university','department']
 




