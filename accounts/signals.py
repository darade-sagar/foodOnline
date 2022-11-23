from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import User,UserProfile



@receiver(post_save,sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        # when user is created then create its user profile
        UserProfile.objects.create(user=instance)
    else:
        try:
            # if we modify user details, then it should be updated in userprofile
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # if any user is created and its userprofile is deleted/not exist
            UserProfile.objects.create(user=instance)

# @receiver(pre_save,sender=User)
# def pre_save_create_profile_receiver(sender, instance, **kwargs):
#     print(instance.username + ' user is created')

# post_save.connect(post_save_create_profile_receiver,sender=User)
