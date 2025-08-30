<<<<<<< HEAD
from django.db import models
=======

from django.conf import settings
from django.db import models
from django.utils import timezone
>>>>>>> d42fc12 (Assignment 2 - Initial commit)

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

<<<<<<< HEAD
=======
def event_default_image_path():
    return 'defaults/event_default.jpg'

>>>>>>> d42fc12 (Assignment 2 - Initial commit)
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
<<<<<<< HEAD
=======
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    image = models.ImageField(upload_to='events/', default=event_default_image_path)
    # RSVP relation via RSVP model
    rsvps = models.ManyToManyField(settings.AUTH_USER_MODEL, through='RSVP', related_name='rsvp_events', blank=True)
>>>>>>> d42fc12 (Assignment 2 - Initial commit)

    def __str__(self):
        return self.name

<<<<<<< HEAD
class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    events = models.ManyToManyField(Event)

    def __str__(self):
        return self.name
=======
class RSVP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.user} -> {self.event}'
>>>>>>> d42fc12 (Assignment 2 - Initial commit)
