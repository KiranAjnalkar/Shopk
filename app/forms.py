from django import forms
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer
from captcha.fields import ReCaptchaField
from captcha.fields import ReCaptchaV2Checkbox


# change password      
class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete' :'current-password', 'autofocus' :True, 'class' : 'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete' :'new-password', 'class' : 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete' :'new-password', 'class': 'form-control'})) 

# forgot password form
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=255, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'} ))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete' :'new-password', 'class' : 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete' :'new-password', 'class': 'form-control'})) 


# profile 
class CustomerProfileForm(forms.ModelForm):
    class Meta:    
        model = Customer   
        fields = ['name', 'mobile_number', 'locality', 'city', 'state', 'zipcode']   
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'} ), 'mobile_number': forms.NumberInput(attrs={'class':'form-control'}), 'locality': forms.TextInput(attrs={'class': 'form-control'} ), 'city': forms.TextInput(attrs={'class': 'form-control'} ), 'state': forms.Select(attrs={'class': 'form-control'} ), 'zipcode': forms.NumberInput(attrs={'class':'form-control'})}
