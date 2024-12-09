import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question, Choice, Vote
# Create your tests here.

class PollsTestCase(TestCase):
    def setUp(self):
        # Create a sample question
        self.question = Question.objects.create(
            question_text="Sample Question?",
            pub_date=timezone.now()  # Provide the current timestamp
        )

        # Create a sample choice for the question
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Sample Choice"
        )

    def test_vote_submission(self):
        # Simulate a POST request to vote for the choice
        response = self.client.post(f'/polls/{self.question.id}/vote/', {'choices': [self.choice.id]})
        
        # Check if the response redirects successfully after voting
        self.assertEqual(response.status_code, 302)  # HTTP 302 means a successful redirect

        # Refresh the choice object to get updated data
        self.choice.refresh_from_db()
        
        # Verify the vote count was incremented
        self.assertEqual(self.choice.votes, 1)

        # Check if a vote record was created with the expected data
        vote = Vote.objects.filter(question=self.question, choice=self.choice).first()
        self.assertIsNotNone(vote)
        self.assertEqual(vote.choice, self.choice)
