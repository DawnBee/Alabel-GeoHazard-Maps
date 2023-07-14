from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms


class UserRegisterForm(UserCreationForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].label = ''
		self.fields['email'].label = ''
		self.fields['password1'].label = ''
		self.fields['password2'].label = ''
		self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
		self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
		self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
		self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-field'}))
	email = forms.EmailField( max_length=50, widget=forms.TextInput(attrs={'class': 'input-field'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field'}))

	class Meta:
		model = User 
		fields = ['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User 
		fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm): 
	class Meta:
		model = Profile 
		fields = ['image','description']
