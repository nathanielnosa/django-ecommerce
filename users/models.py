from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name= models.CharField(max_length=200, null=True, blank= True)
    username= models.CharField(max_length=200, null=True, blank= True)
    email= models.CharField(max_length=200, null=True, blank= True)
    profile_pix = models.ImageField(upload_to='profiles/', default='img/avartar.png')

    def __str__(self):
        return self.name

