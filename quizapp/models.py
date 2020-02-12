from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
	question = models.TextField()
	# answered = models.IntegerField(default=0, blank=True, null=True)
	def __str__(self):
		return self.question

	
class Answer(models.Model):
	question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='questions',blank=True, null=True)
	user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='profile',blank=True, null=True)
	answer = models.CharField(max_length=100)

	def __str__(self):
		return self.answer

class Profile(models.Model):
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50,blank=True,null=True)
	email = models.CharField(max_length=50)
	age = models.IntegerField(blank=True)
	gender = models.CharField(max_length=15)
	country = models.CharField(max_length=30,blank=True,null=True)
	zipcode =models.CharField(max_length=15,blank=True,null=True)
	phone = models.CharField(max_length=15,blank=True,null=True)
	problem = models.CharField(max_length=30,blank=True,null=True)
	sms_concent = models.BooleanField(blank=True,null=True)
	# ontra_contact_id = models.IntegerField(blank=True,null=True)

	def __str__(self):
		return self.firstname
