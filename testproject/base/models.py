from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 1. Model for a Topic Created
class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name

# 2. Model for a Room for a topic had been created by a host
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name
    

# 3. Creating a One-To-Many relationship between Room and Messages
# like when a User or Room gets deleted, all of the content that it relates to will also get deleted
# Using CASCADE to delete all data (msges, room id, participents, etc.) 
class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    room = models.ForeignKey(Room, on_delete=models.CASCADE) 
    body = models.TextField(max_length=None)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', 'created']
    
    def __str__(self) -> str:
        return self.body[0:50]
    