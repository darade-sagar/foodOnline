from .models import SubscribedMails
from accounts.utils import send_notification

# def bulk_mail(mail_subject,template,context):
#     from_email = settings.DEFAULT_FROM_EMAIL
#     context.update({'domain':settings.SITE_URL})
#     message = render_to_string(template,context)
#     to_emails = context['to_email']
#     for id in to_emails:
#         mail = Mail(from_email=from_email,subject=mail_subject,html_content=message, to_emails=id)
#         sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
#         response = sg.send(mail)



def send_news_letter(news):
    mail_subject = 'We have news for you | foodOnline'
    to_emails = SubscribedMails.objects.filter(is_active=True)
    context = {
        'news':news,
        'to_email':to_emails
    }
    template = 'newsletter/newsletter_email.html'
    send_notification(mail_subject,template,context)