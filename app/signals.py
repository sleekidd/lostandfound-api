from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CustomUser
from django.core.mail import send_mail

@receiver(post_save, sender=CustomUser)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:  # Send email only upon user creation
        subject = 'Confirm Your Email Address'
        message = 'Please click the link to confirm your email.'
        send_mail(subject, message, 'your_email@gmail.com', [instance.email])
