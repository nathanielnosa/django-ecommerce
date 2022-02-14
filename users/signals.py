import profile
from . models import Profile
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance

        profile = Profile.objects.create(
            user = user,
            email = user.email,
            name = user.first_name,
            username = user.username,
        )
        subject = 'Welcome to my ecommerce page'
        body = f'Welcome to my ecommerce page, thanks for registering'
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )

def updateprofile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.username = profile.username
        user.email = profile.email
        user.first_name = profile.name
        user.save()



post_save.connect(createProfile, sender=User)
post_save.connect(updateprofile, sender=Profile)