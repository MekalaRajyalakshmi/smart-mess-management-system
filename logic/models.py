from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('cook', 'Cook'),
        ('rep', 'Mess Representative'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Menu(models.Model):
    MEAL_TYPES = [('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')]
    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)
    items = models.TextField()  # Store as comma-separated or plain text

    class Meta:
        unique_together = ('date', 'meal_type')

class Confirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')])
    will_eat = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'date', 'meal_type')