from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    skills = models.TextField()         # store as comma-separated string or JSON
    interests = models.TextField()
    year = models.CharField(max_length=20)
    branch = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)

    # for graph algorithms later
    # you can convert this easily to list: skills.split(',')
    def skills_list(self):
        return [s.strip() for s in self.skills.split(",")]

    def interest_list(self):
        return [i.strip() for i in self.interests.split(",")]

    def __str__(self):
        return self.user.username
