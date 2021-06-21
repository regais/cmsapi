from django.db import models
from django.contrib.auth.models import User, UserManager
from django.urls import reverse


from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    app_label = 'Profile'
    phone     = models.CharField(max_length=12)
    address   = models.CharField(max_length=200, blank=True)
    city      = models.CharField(max_length=30,  blank=True)
    state     = models.CharField(max_length=30,  blank=True)    
    country   = models.CharField(max_length=30,  blank=True)
    zip_code = models.CharField( max_length=6, default = "600000")
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):  
        return self.user.username

    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if  created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    
    
# Create your models here.
# The layout of the CMS has been put out here along with field validations.
#reverse_lazy has been imported here for the purpose of redirection upon successful submission of a blog article.
class ContentModel(models.Model):
     app_label = 'ContentModel'
     author =  models.ForeignKey(User, on_delete=models.CASCADE)
     title = models.CharField(max_length=30)
     body = models.CharField(max_length=300)
     summary = models.CharField(max_length=60)
     document = models.FileField(upload_to = 'documents/')
     categories = models.CharField(max_length=10, blank=False)     
      
    
     def __str__(self):
        return self.title
    
     def get_absolute_url(self):
         return reverse('home') 
            
    