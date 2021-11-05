from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from ckeditor.fields import RichTextField
from django.urls import reverse

# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)



class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    snippet = models.CharField(max_length=300, default="Default snippet text")
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    header_image = models.ImageField(null=True,blank=True,upload_to = "images/")
    content = RichTextField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    post_id = models.AutoField(primary_key=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=(str(self.id)))
    


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments',default="")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    comment_id = models.AutoField(primary_key=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)