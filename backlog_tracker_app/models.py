from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 

    def __str__(self): 
        return self.user.username

class ShowBacklog(models.Model): 
    name = models.CharField(max_length=100) 
    genre = models.CharField(max_length=100) 
    summary = models.TextField() 
    release_date = models.DateField() 
    image_url = models.CharField(max_length=100, default='') 

    current_episode = models.IntegerField(default=0) 
    max_episodes = models.IntegerField(default=0) 

    user_rating = models.IntegerField(default=0)

    #Many-to-one relationship to 'User' table
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self): 
        return self.name

    class Meta: 
        ordering = ['name']

class EpisodeLog(models.Model): 
    name = models.CharField(max_length=100) 
    summary = models.TextField() 
    release_date = models.DateField() 
    is_complete = models.BooleanField() 

    # Many-to-one relationship to 'ShowBacklog' table
    show_backlog = models.ForeignKey(ShowBacklog, on_delete=models.CASCADE)

    def __str__(self): 
        return self.name