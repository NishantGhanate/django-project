from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django_project.settings import EMAIL_HOST_USER


def send_worker_email(data):
        email_subject = data.get('email_subject')
        context = {
                'username': data.get('username') ,
                'email_message' : data.get('email_message')
                } 
        html_content = render_to_string('test_email.html', context)
        to_email = data.get('email')
        text_content =''
        msg = EmailMultiAlternatives(
                email_subject, 
                text_content,
                EMAIL_HOST_USER, 
                [to_email]
        )
        msg.attach_alternative(html_content, "text/html")
        return msg.send()
