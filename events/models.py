from django.db import models

class Event(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    date = models.DateField()

    venue = models.CharField(max_length=200)

    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    def __str__(self):
        return self.title
    
class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    roll_number = models.CharField(max_length=10)
    attended = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name