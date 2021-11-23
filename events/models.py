from django.db import models
from django.contrib.auth.models import User

class Venue(models.Model):
	name 	 	  = models.CharField('Venue Name', max_length = 120)
	address  	  = models.CharField(max_length = 120)
	zip_code      = models.CharField('Zip Code', max_length = 20)
	phone 	 	  = models.CharField('Contact Phine', max_length = 60, blank = True)
	web 	 	  = models.URLField('Web_address', blank = True)
	email_address = models.EmailField('Email', blank = True)
	owner 		  = models.IntegerField('Venue Owner', blank = False, default = 1)

	def __str__(self):
		return self.name


class MyClubUser(models.Model):
	first_name = models.CharField('Name', max_length = 50)
	last_name  = models.CharField('Surname', max_length = 50)
	email 	   = models.EmailField('User Email')

	def __str__(self):
		return self.first_name + ' ' + self.last_name 


class Event(models.Model):
	name 	    = models.CharField('Event Name', max_length = 120)
	event_date  = models.DateTimeField('Event Time')
	venue 		= models.ForeignKey(Venue, blank = True, null = True, on_delete = models.CASCADE)
	#venue 		= models.CharField(max_length = 120)
	manager 	= models.ForeignKey(User, blank = True, null = True, on_delete = models.SET_NULL)
	description = models.TextField(blank = True)
	attendees 	= models.ManyToManyField(MyClubUser, blank = True)

	def __str__(self):
		return self.name
