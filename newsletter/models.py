from django.db import models
from accounts.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class SubscribedMails(models.Model):
    email = models.EmailField(max_length=50,blank=False,unique=True)
    is_active = models.BooleanField(default=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Subscribed Emails'

    def __str__(self):
        return self.email

class News(models.Model):
    title = models.CharField(max_length=100,blank=False)
    slug = models.CharField(max_length=200,default=None,unique=True)
    short_description = models.TextField(max_length=200,blank=False)
    long_description = RichTextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title