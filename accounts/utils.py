from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def detectUser(user):
    if user.role==1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role==2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superuser:
        redirectUrl = '/admin'
        return redirectUrl



def send_verification_email(request, user, mail_subject, template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(template,{
        'user':user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)), # this will create unique value of user
        'token': default_token_generator.make_token(user), # this is unique value generated each time
        'domain':settings.SITE_URL,
    })
    
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email=from_email,to=[to_email])
    mail.content_subtype = 'html'
    mail.send()



def send_notification(mail_subject,template,context):
    from_email = settings.DEFAULT_FROM_EMAIL
    context.update({'domain':settings.SITE_URL})
    message = render_to_string(template,context)
    to_emails = context['to_email']
    for id in to_emails:
        mail = EmailMessage(mail_subject, message, from_email=from_email,to=[id])
        mail.content_subtype = 'html'
        mail.send()

