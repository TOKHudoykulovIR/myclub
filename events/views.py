from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin
import csv
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User



# creating pdf file
def venue_pdf(request):
	buf = io.BytesIO()

	c = canvas.Canvas(buf, pagesize = letter, bottomup = 0)

	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont('Helvetica', 14)
	
	venues = Venue.objects.all()
	
	lines = []
	
	for venue in venues:
		lines.append(venue.name),
		lines.append(venue.address),
		lines.append(venue.zip_code),
		lines.append(venue.phone),
		lines.append(venue.web),
		lines.append(venue.email_address)
		lines.append(' ')
	
	for line in lines:
		textob.textLine(line)
	
	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	return FileResponse(buf, as_attachment = True, filename = 'venues.pdf')



# creating csv file
def venue_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=venues.csv'
	
	writer = csv.writer(response)
	
	venues = Venue.objects.all()
	
	# adding headings to csv file
	writer.writerow(['Venue Name', 'Address', 'Zip code', 'Phone', 'Web', 'Email'])

	for venue in venues:
		writer.writerow([venue.name,venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])
	
	return response



# creating text file
def venue_text(request):
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=venues.txt'
	
	venues = Venue.objects.all()
	
	lines = []
	
	for venue in venues:
		lines.append(f'{venue}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n')
	# lines = ['Cover1\n', 'Cover2']
	
	response.writelines(lines)
	
	return response



# deleting venue from db
def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk = venue_id)
	if request.user.id == venue.owner or request.user.is_superuser:
		venue.delete()
		messages.success(request, ('Venue successfully deleted'))
		return redirect('list-venues')
	else:
		messages.success(request, ('You are not rightful owner of this venue'))
		return redirect('list-venues')



# deleting event from db
def delete_event(request, event_id):
	event = Event.objects.get(pk = event_id)
	if request.user == event.manager or request.user.is_superuser:
		event.delete()
		messages.success(request, ('Event successfully deleted'))
		return redirect('list-events')
	else:
		messages.success(request, ('You are not rightful owner of this event'))
		return redirect('list-events')



# updating event in db
def update_event(request, event_id):
	event = Event.objects.get(pk = event_id)
	if request.user.is_superuser:
		form = EventFormAdmin(request.POST or None, instance = event)
	else:
		form = EventForm(request.POST or None, instance = event)
	
	if form.is_valid():
		form.save()
		return redirect('list-events')
	context = {
		'form': form,
		'event': event
	}
	return render(request, 'events/update_event.html', context)



# adding event to db
def add_event(request):
	submitted = False
	if request.method == 'POST':
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/add_event?submitted=True')

		else:
			form = EventForm(request.POST)
			if form.is_valid():
				event = form.save(commit=False) # пока не сохраняй
				event.manager = request.user
				event.save()
				return HttpResponseRedirect('/add_event?submitted=True')
	else:
		if request.user.is_superuser:
			form = EventFormAdmin
		else:
			form = EventForm
		if 'submitted' in request.GET:
			submitted = True
	context = {
		'form': form,
		'submitted': submitted
	}
	return render(request, 'events/add_event.html', context)



# updating venue in db
def update_venue(request, venue_id):
	venue = Venue.objects.get(pk = venue_id)
	
	form = VenueForm(request.POST or None, instance = venue)
	print(request.user)
	if request.user.id == venue.owner or request.user.is_superuser:
		if form.is_valid():
			messages.success(request, ('Venue successfully updated'))
			form.save()
			return redirect('list-venues')
	else:
		messages.success(request, ('You are not creator of this venue'))
		return redirect('list-venues')
	context = {
		'venue': venue,
		'form': form
	}
	return render(request, 'events/update_venue.html', context)



# searching venue
def search_venues(request):
	if request.method == 'POST':
		searched = request.POST.get('searched')
		venues = Venue.objects.filter(name__contains = searched)
		return render(request, 'events/search_venues.html', {'searched': searched, 'venues': venues})
	else:
		return render(request, 'events/search_venues.html', {})
	


# showing venues by their id
def show_venue(request, venue_id):
	venue = Venue.objects.get(pk = venue_id)
	venue_owner = User.objects.get(pk = venue.owner)
	context = {
		'venue': venue,
		'venue_owner': venue_owner
	}
	return render(request, 'events/show_venue.html', context)



# list of venues
def list_venues(request):
	#venue_list = Venue.objects.all().order_by('name')
	#venue_list = Venue.objects.all()

	p = Paginator(Venue.objects.all(), 4)
	page = request.GET.get('page')
	venues = p.get_page(page)
	context = {
		#'venue_list': venue_list,
		'venues': venues
	}
	return render(request, 'events/venues.html', context)



# adding venue to db
def add_venue(request):
	submitted = False
	
	if request.method == 'POST':
		form = VenueForm(request.POST)
		if form.is_valid():
			#form.save()
			venue = form.save(commit=False) # пока не сохраняй
			venue.owner = request.user.id
			venue.save()
			return HttpResponseRedirect('/add_venue?submitted=True')
	else:
		form = VenueForm
	
	if 'submitted' in request.GET:
		submitted = True
	context = {
		'form': form,
		'submitted': submitted
	}
	return render(request, 'events/add_venue.html', context)



# list of events
def all_events(request):
	event_list = Event.objects.all()
	context = {
		'event_list': event_list
	}
	return render(request, 'events/event_list.html', context)



# creating calendar, date, time ... in home page
def home(request, year = datetime.now().year, month = datetime.now().strftime('%B')):
	
	month = month.capitalize()
	#convert month from name to number
	month_num = list(calendar.month_name).index(month)
	month_num = int(month_num)
	
	cal = HTMLCalendar().formatmonth(year, month_num)
	
	now = datetime.now()
	
	current_year = now.year
	current_time = now.strftime('%H:%M')
	context = {
		'year': year,
		'month': month,
		'month_num': month_num,
		'cal': cal,
		'current_year': current_year,
		'time': current_time,
	}
	return render(request, 'events/home.html', context)
