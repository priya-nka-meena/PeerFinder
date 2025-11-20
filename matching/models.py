from django.db import models

# Create your models here.


class StudentProfile(models.Model):
    name = models.CharField(max_length=100)
    skills = models.JSONField()
    interests = models.JSONField()
    year = models.IntegerField()
    branch = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    gmail = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
