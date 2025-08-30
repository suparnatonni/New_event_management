
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate'),
    path('rsvp/<int:event_id>/', views.rsvp_event, name='rsvp'),
    path('dashboard/participant/', views.participant_dashboard, name='participant_dashboard'),
    path('dashboard/organizer/', views.organizer_dashboard, name='organizer_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
]
