
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import RSVP

User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_email_on_signup(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = default_token_generator.make_token(instance)
        subject = 'Activate your account'
        message = f'Please activate your account using the link: /events/activate/{uid}/{token}/'
        send_mail(subject, message, None, [instance.email])

@receiver(post_save, sender=RSVP)
def send_rsvp_notification(sender, instance, created, **kwargs):
    if created:
        # email to participant
        send_mail(
            f'RSVP confirmation for {instance.event.name}',
            f'You have successfully RSVP\'d to {instance.event.name} ({instance.event.date}).',
            None,
            [instance.user.email]
        )
        # email to organizer
        if instance.event.organizer and instance.event.organizer.email:
            send_mail(
                f'New RSVP for {instance.event.name}',
                f'{instance.user.get_full_name() or instance.user.username} RSVP\'d to {instance.event.name}.',
                None,
                [instance.event.organizer.email]
            )
