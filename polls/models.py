from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import datetime


class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(1)

	def __str__(self) -> str:
		return self.question_text


class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self) -> str:
		return self.choice_text


class Vote(models.Model):
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
	voter = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self) -> str:
		return f'{self.voter} voted for {self.choice}'