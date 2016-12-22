from django.core.files import File
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import pre_save
from blog.utils import thumbnail


class Post(models.Model):
    title = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    content = models.TextField()
    photo = models.ImageField(blank=True, upload_to='blog/post/%Y/%m/%d')
    author = models.CharField(max_length=20)
    tags = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tag_set = models.ManyToManyField('Tag', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return '/blog/{}'.format(self.pk)
        return reverse('blog:post_detail', args=[self.pk])

def on_pre_save_post(sender, **kwargs):
    post = kwargs['instance']
    if post.photo:
        max_width = 300
        if post.photo.width > max_width or post.photo.height > max_width:
            processed_f = thumbnail(post.photo.file, max_width, max_width)
            post.photo.save(post.photo.name, File(processed_f))

pre_save.connect(on_pre_save_post, sender=Post)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

