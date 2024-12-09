from django.db import models
from django.contrib.auth.models import User

# Create your models(tables, each attribute is column) here.

class Question(models.Model): #parent
    question_text = models.CharField(max_length=200) #column
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model): #tracks each choice
    question = models.ForeignKey(Question, on_delete = models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length = 200)
    meal = models.CharField(max_length = 50, null = True, blank = True)
    votes = models.IntegerField(default = 0) #tracks votes of each choice w/o associating w/ any user

    def __str__(self):
        return self.choice_text
    
class Vote(models.Model): #tracks voting detz for Aaron+ensures every choice is tied to ip
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete = models.CASCADE)
    ip_address = models.GenericIPAddressField()
    vote_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('question', 'ip_address')

    def __str__(self):
        return f"Vote for {self.choice.choice_text} at {self.vote_time} by {self.ip_address}"
    
#going to https://127.0.1:8000/admin will lead to login page