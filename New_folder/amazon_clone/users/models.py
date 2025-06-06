from django.db import models
from django.contrib.auth.models import User

# We don't need custom models for users as we're using Django's built-in User model
# But if you want to extend it, you could create a profile model:

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields here if needed
    
    def __str__(self):
        return f"{self.user.username}'s Profile"