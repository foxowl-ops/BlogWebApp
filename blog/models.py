from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status = 'P')

class Post(models.Model):
    statuses = [("D","Draft"), ("P","Published")]
    title = models.CharField(max_length=250)
    content = HTMLField()
    status = models.CharField(max_length=1, choices=statuses, default = "D" )
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="categories")
    image = models.ImageField(upload_to='blog/',blank= True)
    slug = models.SlugField(blank = True, unique = True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    objects = models.Manager()
    post_man = PostQuerySet.as_manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        print(self._state.adding)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post-detail", args = [self.slug])

