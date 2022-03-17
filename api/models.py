import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
	def create_user(self, email, username, password=None): #pass All required fields
		if not email:
			raise ValueError("Users must have an email adress")
		if not username:
			raise ValueError("Users must have an username")

		user = self.model(
			email = self.normalize_email(email),
			username = username
		)
  
		user.set_password(password)
		user.save(using=self._db)
		return user 

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email = self.normalize_email(email),
			password = password,
			username = username
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user
	



class Account(AbstractBaseUser):
    #Required Fields
	email				= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username			= models.CharField(max_length=30, unique=True)
	date_joined			= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login			= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin			= models.BooleanField(default=False)
	is_active			= models.BooleanField(default=True)
	is_staff			= models.BooleanField(default=False)
	is_superuser		= models.BooleanField(default=False)
 
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
 
	objects = AccountManager()
 
	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

class Category(models.Model):
    text 				= models.CharField(max_length=100)
    date_added			= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    
    def __str__(self):
        return self.text

class Question(models.Model):
    statement           = models.CharField(max_length=300)
    date_selected		= models.DateField(default=datetime.date(2014, 10, 9))
    date_added			= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    category 			= models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.statement

class Answer(models.Model):
    response            = models.CharField(max_length=200)
    is_correct 			= models.BooleanField(default=False)
    question 			= models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.response
    
class Choice(models.Model):
    question 			= models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    account 			= models.ForeignKey(Account, on_delete=models.CASCADE)
    date 				= models.DateTimeField(verbose_name='date answered', auto_now_add=True)
    is_correct 			= models.BooleanField(default=False)
    
    def __str__(self):
        return self.question.statement+' '+self.account.username+' '+str(self.is_correct)