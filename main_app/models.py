from django.db import models
from django.urls import reverse

class Mood(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

def __str__(self):
    return f'{self.name} ({self.id})'

def get_absolute_url(self):
    return reverse('detail', kwargs={'mood_id': self.id})