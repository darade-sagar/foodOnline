from django.db import models

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
