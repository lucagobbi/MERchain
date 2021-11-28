from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(default='default.jpg', upload_to='profile_imgs', null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def profile_imgURL(self):
        try:
            url = self.profile_img.url
        except:
            url = ''
        
        return url