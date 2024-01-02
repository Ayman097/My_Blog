from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.

class PublishedManager(models.Manager):
    '''
    Creating model managers
    The default manager for every model is the 'objects' manager. This manager retrieves all the objects in the database. so Here will create custom managers
    this custom managers allow to me retrieve all posts that have a PUBLISHED status.

    Post.published.filter(title__startswith='Who') / .all() and so on
    '''
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        PUBLISHED = 'PB', 'Published'

        '''
        In Shell if I try these

        Post.Status.choices
        [('DF', 'Draft'), ('PB', 'Published')]

        Post.Status.labels
        ['Draft', 'Published']

        Post.Status.values
        ['DF', 'PB']

        Post.Status.names
        ['DRAFT', 'PUBLISHED']
        '''

    title = models.CharField(max_length=255)
    # To retrieve single posts with the combination of publication date and slug
    slug = models.SlugField(max_length=255, unique_for_date='publish') # so we need to ensure that no post can be stored in the database with the same slug and publish date as an existing post
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateField(default=timezone.now)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices = Status.choices, default = Status.DRAFT)

    objects = models.Manager() # The default manager
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager() # tags manager will allow you to add, retrieve, and remove tags from Post objects.

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                    self.publish.month,
                                                    self.publish.day,
                                                    self.slug
                                                ]
                        )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
        models.Index(fields=['created']),
        ]
        
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
