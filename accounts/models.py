from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    skills = models.TextField()
    interests = models.TextField()
    year = models.CharField(max_length=20)
    branch = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def skills_list(self):
        return [s.strip() for s in self.skills.split(",") if s.strip()]

    def interest_list(self):
        return [i.strip() for i in self.interests.split(",") if i.strip()]

    def __str__(self):
        return self.user.username


# -----------------------------------------------------
# INVITATION SYSTEM
# -----------------------------------------------------
class Invitation(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    sender = models.ForeignKey(
        User,
        related_name="sent_invitations",
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name="received_invitations",
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')  # 🔥 Prevent duplicate invites

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username} [{self.status}]"
