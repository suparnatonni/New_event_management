
from django.conf import settings
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

def event_default_image_path():
    return 'defaults/event_default.jpg'

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    image = models.ImageField(upload_to='events/', default=event_default_image_path)
    # RSVP relation via RSVP model
    rsvps = models.ManyToManyField(settings.AUTH_USER_MODEL, through='RSVP', related_name='rsvp_events', blank=True)

    def __str__(self):
        return self.name

class RSVP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.user} -> {self.event}'
