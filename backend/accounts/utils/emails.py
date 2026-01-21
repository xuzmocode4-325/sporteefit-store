# core/email_utils.py
import os
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import user_tokenizer_generate

def send_verification_email(request, user):
    platform_name = os.getenv("PLATFORM", "")
    recipient_email = user.email
    subject = f"Welcome to the {platform_name} Platform" if platform_name else "Welcome to our Platform"
    current_site = get_current_site(request)
    html_message = render_to_string(
        "emails/registration/email-verification.html", 
        {
            "username": user.username,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": user_tokenizer_generate.make_token(user),
            "platform": platform_name
        }
    )
    #plain_message = strip_tags(html_message)  # fallback text-only version
    email = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=None,  # uses DEFAULT_FROM_EMAIL
        to=[recipient_email],
    )
    email.content_subtype = "html"  # send as HTML
    email.send()


def send_password_reset_email(request, user):
    recipient_email = user.email
    subject = "Password Update Request Recieved"
    current_site = get_current_site(request)
    html_message = render_to_string(
        "emails/password/password-restet.html", 
        {
            "username": user.username,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": user_tokenizer_generate.make_token(user)
        }
    )
    plain_message = strip_tags(html_message)  # fallback text-only version
    email = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=None,  # uses DEFAULT_FROM_EMAIL
        to=[recipient_email],
    )
    email.content_subtype = "html"  # send as HTML
    email.send()