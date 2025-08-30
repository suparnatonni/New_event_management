
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
