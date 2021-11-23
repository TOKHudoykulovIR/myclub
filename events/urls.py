from django.urls import path
from events.views import (
    home, 
    all_events, 
    add_venue, 
    list_venues, 
    show_venue, 
    search_venues, 
    update_venue, 
    add_event, 
    update_event, 
    delete_event,
    delete_venue,
    venue_text,
    venue_csv,
    venue_pdf,
    )


urlpatterns = [
    path('', home, name = 'home'),
    path('events', all_events, name = 'list-events'),
    path('<int:year>/<str:month>/', home, name = 'home'),
    path('add_venue/', add_venue, name = 'add-venue'),
    path('list_venues/', list_venues, name = 'list-venues'),
    path('show_venue/<venue_id>', show_venue, name = 'show-venue'),
    path('search_venues/', search_venues, name = 'search-venues'),
    path('update_venue/<venue_id>', update_venue, name = 'update-venue'),
    path('add_event/', add_event, name = 'add-event'),
    path('update_event/<event_id>', update_event, name = 'update-event'),
    path('delete_event/<event_id>', delete_event, name = 'delete-event'),
    path('delete_venue/<venue_id>', delete_venue, name = 'delete-venue'),
    path('venue_text', venue_text, name = 'venue-text'),
    path('venue_csv', venue_csv, name = 'venue-csv'),
    path('venue_pdf', venue_pdf, name = 'venue-pdf'),
]