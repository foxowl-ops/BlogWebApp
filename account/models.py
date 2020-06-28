from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth.models import Group
# Create your models here.

class User(AbstractUser):
    gro = [("R","Reader"), ("A","Author")]
    email = models.EmailField(unique=True)
    pic = models.ImageField(upload_to="account/", blank = True)
    bio = models.TextField(blank=True)
    group = models.CharField(max_length=1,choices=gro, default = "R")
    REQUIRED_FIELDS =("email",)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("detailuser", args = [self.id])

