from django import forms
from django.forms import ModelForm
from .models import Venue, Event

class VenueForm(ModelForm):
	class Meta:
		model = Venue
		fields = ('name', 'address','zip_code','phone','web','email_address')
		labels = {
			'name': '',
			'address': '',
			'zip_code': '',
			'phone': '',
			'web': '',
			'email_address': ''
		}
		widgets = {
			'name': 		 forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
			'address': 		 forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
			'zip_code': 	 forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
			'phone': 		 forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
			'web': 			 forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Web'}),
			'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
		}



class EventFormAdmin(ModelForm):
	class Meta:
		model = Event
		fields = '__all__'
		labels = {
			'name': '',
			'event_date': '',
			'venue': 'Venue',
			'manager': 'Manager',
			'description': '',
			'attendees': 'Attendees'
		}
		widgets = {
			'name': 	   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
			'event_date':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
			'venue': 	   forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
			'manager': 	   forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
			'attendees':   forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'})
		}


# user form
class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ('name','event_date','venue','description','attendees')
		labels = {
			'name': '',
			'event_date': '',
			'venue': 'Venue',
			'description': '',
			'attendees': 'Attendees'
		}
		widgets = {
			'name': 	   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
			'event_date':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
			'venue': 	   forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
			'attendees':   forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'})
		}