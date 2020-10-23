from django.db import models
import re

class UserManager(models.Manager):
	def reg_validator(self,postData):
		errors = {}
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if len(postData['first_name']) < 3:
			errors['first_name'] = "First Name must be at least 3 characters."
		if len(postData['last_name']) < 3:
			errors['last_name'] = "Last Name must be at least 3 characters."
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = 'Invalid Email'
		if len(postData['password']) < 8:
			errors['password'] = "Password must be at least 8 characters."
		if postData['password'] != postData['password_confirm']:
			errors['password_confirm'] = "Passwords do not match."
		return errors
	def update_validator(self, postData):
		errors = {}
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if len(postData['first_name']) < 3:
			errors['first_name'] = "First Name must be at least 3 characters."
		if len(postData['last_name']) < 3:
			errors['last_name'] = "Last Name must be at least 3 characters."
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = 'Invalid Email'
		return errors

	def login_validator(self, postData):
		errors = {}
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if not EMAIL_REGEX.match(postData['login_email']):
			errors['login'] = "Invalid Email/Password."
		if len(postData['login_password']) < 8:
			errors['login_password'] = "Invalid Email/Password"
		return errors

	def basic_validator(self, postData):
		errors = {}
		if len(postData['author']) < 3:
			errors['author'] = "Author's name must be at least 3 characters"
		if len(postData['quote']) < 10:
			errors['quote'] = "Quote must be at least 10 characters"
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_At = models.DateTimeField(auto_now=True)
	objects = UserManager()


class Quote(models.Model):
	Author = models.CharField(max_length=500)
	Quote = models.CharField(max_length=30)
	posted_by = models.ForeignKey(User, related_name='Quotes', on_delete = models.CASCADE)
	likes = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
	
	