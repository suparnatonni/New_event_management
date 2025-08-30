<<<<<<< HEAD
from django import forms
from .models import Event, Participant, Category
=======

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Event

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
>>>>>>> d42fc12 (Assignment 2 - Initial commit)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
<<<<<<< HEAD
        fields = '__all__'

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
=======
        fields = ['name','description','date','time','location','category','image']
>>>>>>> d42fc12 (Assignment 2 - Initial commit)
