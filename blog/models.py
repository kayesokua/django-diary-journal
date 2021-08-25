from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
import datetime

STATUS = ((0, "Draft"), (1, "Publish"))

class Post(models.Model, HitCountMixin):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='blog', default='default.jpg')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = TaggableManager() 
    total_likes = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("post_detail", kwargs={"slug": str(self.slug)})

class PostViews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='blog_views')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40, null=True)
    created = models.DateTimeField(default=datetime.datetime.now())

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    url = models.URLField(max_length=100,default=False)
    body = models.TextField(max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.name)

class EditableFields(models.Model):
    field_id = models.CharField(max_length=80)
    field_title = models.CharField(max_length=255)
    field_url = models.URLField(max_length=255,default="http://")
    field_content = models.TextField()
    image = models.ImageField(upload_to='uploaded', default='default.jpg')
    
    def __str__(self):
        return self.field_id

class SociaLinks(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255,default="http://")

    def __str__(self):
        return self.name 