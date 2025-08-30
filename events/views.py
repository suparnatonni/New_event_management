<<<<<<< HEAD
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm
from django.db.models import Count,Sum
from django.utils.dateparse import parse_date
from django.utils import timezone
from datetime import date
from django.db.models import Q





def event_list(request):
    events = Event.objects.select_related('category').all()
    return render(request, 'events/event_list.html', {'events': events})

def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})



def participant_list(request):
    participants = Participant.objects.all()
    return render(request, 'events/participant_list.html', {'participants': participants})

def participant_create(request):
    form = ParticipantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('participant_list')
    return render(request, 'events/participant_form.html', {'form': form})

def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    form = ParticipantForm(request.POST or None, instance=participant)
    if form.is_valid():
        form.save()
        return redirect('participant_list')
    return render(request, 'events/participant_form.html', {'form': form})

def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'events/participant_confirm_delete.html', {'participant': participant})



def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})

def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'events/category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'events/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'events/category_confirm_delete.html', {'category': category})



def event_list(request):
    events = Event.objects.select_related('category').all()
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event.objects.prefetch_related('participant_set'), pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})




def dashboard(request):
    total_events = Event.objects.count()
    total_participants = Participant.objects.aggregate(count=Count('id'))['count']

    context = {
        'total_events': total_events,
        'total_participants': total_participants,
    }
    return render(request, 'events/dashboard.html', context)


def filtered_events(request):
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    events = Event.objects.all()

    if category_id:
        events = events.filter(category_id=category_id)

    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    return render(request, 'events/event_filtered_list.html', {'events': events})


# events/views.py


def dashboard(request):
    today = date.today()

    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    upcoming_events = Event.objects.filter(date__gt=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    todays_events = Event.objects.filter(date=today)

    # For dynamic filtering (based on button click)
    filter_type = request.GET.get("filter", "all")
    if filter_type == "upcoming":
        filtered_events = Event.objects.filter(date__gt=today)
    elif filter_type == "past":
        filtered_events = Event.objects.filter(date__lt=today)
    else:
        filtered_events = Event.objects.all()

    context = {
        "total_events": total_events,
        "total_participants": total_participants,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "todays_events": todays_events,
        "filtered_events": filtered_events,
        "filter_type": filter_type,
    }
    return render(request, "events/dashboard.html", context)


# events/views.py

def search_events(request):
    query = request.GET.get('q')
    events = Event.objects.all()

    if query:
        events = events.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )

    return render(request, 'events/event_search.html', {'events': events, 'query': query})
=======

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.urls import reverse
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import SignUpForm, EventForm
from .models import Event, RSVP

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            participant_group, _ = Group.objects.get_or_create(name='Participant')
            user.groups.add(participant_group)
            # send activation email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('events/account_activation_email.txt', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(subject, message, None, [user.email])
            return render(request, 'events/please_confirm.html')
    else:
        form = SignUpForm()
    return render(request, 'events/signup.html', {'form': form})

def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        from django.contrib.auth import get_user_model
        user = get_user_model().objects.get(pk=uid)
    except Exception:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'events/activation_success.html')
    else:
        return render(request, 'events/activation_invalid.html')

@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    rsvp, created = RSVP.objects.get_or_create(user=user, event=event)
    if created:
        # confirmation email sent by signal too
        return redirect('events:participant_dashboard')
    else:
        return HttpResponse('You have already RSVP\'d to this event.', status=400)

@login_required
def participant_dashboard(request):
    user = request.user
    rsvped_events = user.rsvp_events.all()
    return render(request, 'events/participant_dashboard.html', {'events': rsvped_events})

@login_required
def organizer_dashboard(request):
    user = request.user
    events = user.organized_events.all()
    return render(request, 'events/organizer_dashboard.html', {'events': events})

@login_required
def admin_dashboard(request):
    events = Event.objects.all()
    return render(request, 'events/admin_dashboard.html', {'events': events})
>>>>>>> d42fc12 (Assignment 2 - Initial commit)
