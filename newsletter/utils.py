from .models import SubscribedMails
from accounts.utils import send_notification

def send_news_letter(news):
    mail_subject = 'We have news for you | foodOnline'
    to_emails = SubscribedMails.objects.filter(is_active=True)
    context = {
        'news':news,
        'to_email':to_emails
    }
    template = 'newsletter/newsletter_email.html'
    send_notification(mail_subject,template,context)