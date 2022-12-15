from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User,related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile,related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_licence = models.ImageField(upload_to='vendor/licence')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved':self.is_approved,
                }
                if self.is_approved==True:
                    # send congratulations notification
                    mail_subject = 'Congratulations! Your restaurant has been approved | foodOnline'
                    send_notification(mail_subject,template, context)
                else:
                    # send sorry notification
                    mail_subject = 'Restaurant Registration Status | foodOnline'
                    send_notification(mail_subject,template, context)

        return super(Vendor, self).save(*args, **kwargs)


DAYS = [
    # (values,("display label")),
    (1,("Monday")),
    (2,("Tuesday")),
    (3,("Wednesday")),
    (4,("Thursday")),
    (5,("Friday")),
    (6,("Saturday")),
    (7,("Sunday")),
]

HOUR_OF_DAY_24 = [
    ('12:00 AM', '12:00 AM'),
    ('12:30 AM', '12:30 AM'),
    ('01:00 AM', '01:00 AM'),
    ('01:30 AM', '01:30 AM'),
    ('02:00 AM', '02:00 AM'),
    ('02:30 AM', '02:30 AM'),
    ('03:00 AM', '03:00 AM'),
    ('03:30 AM', '03:30 AM'),
    ('04:00 AM', '04:00 AM'),
    ('04:30 AM', '04:30 AM'),
    ('05:00 AM', '05:00 AM'),
    ('05:30 AM', '05:30 AM'),
    ('06:00 AM', '06:00 AM'),
    ('06:30 AM', '06:30 AM'),
    ('07:00 AM', '07:00 AM'),
    ('07:30 AM', '07:30 AM'),
    ('08:00 AM', '08:00 AM'),
    ('08:30 AM', '08:30 AM'),
    ('09:00 AM', '09:00 AM'),
    ('09:30 AM', '09:30 AM'),
    ('10:00 AM', '10:00 AM'),
    ('10:30 AM', '10:30 AM'),
    ('11:00 AM', '11:00 AM'),
    ('11:30 AM', '11:30 AM'),
    ('12:00 PM', '12:00 PM'),
    ('12:30 PM', '12:30 PM'),
    ('01:00 PM', '01:00 PM'),
    ('01:30 PM', '01:30 PM'),
    ('02:00 PM', '02:00 PM'),
    ('02:30 PM', '02:30 PM'),
    ('03:00 PM', '03:00 PM'),
    ('03:30 PM', '03:30 PM'),
    ('04:00 PM', '04:00 PM'),
    ('04:30 PM', '04:30 PM'),
    ('05:00 PM', '05:00 PM'),
    ('05:30 PM', '05:30 PM'),
    ('06:00 PM', '06:00 PM'),
    ('06:30 PM', '06:30 PM'),
    ('07:00 PM', '07:00 PM'),
    ('07:30 PM', '07:30 PM'),
    ('08:00 PM', '08:00 PM'),
    ('08:30 PM', '08:30 PM'),
    ('09:00 PM', '09:00 PM'),
    ('09:30 PM', '09:30 PM'),
    ('10:00 PM', '10:00 PM'),
    ('10:30 PM', '10:30 PM'),
    ('11:00 PM', '11:00 PM'),
    ('11:30 PM', '11:30 PM')
]


class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS,unique=True)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day','-from_hour')
        unique_together = ('day','from_hour','to_hour')
        
    def __str__(self):
        val = DAYS[self.day-1][1]
        return val