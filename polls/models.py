from django.db import models
from django.contrib.auth.models import User

# Create your models(tables, each attribute is column) here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    BREAKFAST = 'Breakfast'
    LUNCH = 'Lunch'
    DINNER = 'Dinner'

    MEAL_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    ]

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    meal = models.CharField(max_length=10, choices=MEAL_CHOICES)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.choice_text} ({self.meal})"
    
class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user_ip = models.GenericIPAddressField()  # To track votes per user (optional)
    voted_at = models.DateTimeField(auto_now_add=True)  # To track when the vote was cast

    def __str__(self):
        return f"Vote for {self.choice.choice_text} by {self.user_ip} at {self.voted_at}"
    
#going to https://127.0.1:8000/admin will lead to login page