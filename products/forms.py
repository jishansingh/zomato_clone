from django import forms
from .choices import CHOICES
from .models import Restraunt,UserProfile
class AddRestraunt(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    owner_name=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    address=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    city=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    state=forms.ChoiceField(choices=[CHOICES], required=True,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    veg=forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'fancy-checkbox-success'}))
    image=forms.ImageField()
    delivery_time=forms.IntegerField()
    mode_of_payment=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    offer=forms.CharField(required=False,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    cuisines=forms.CharField(required=False,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    class Meta:
        model=Restraunt
        fields=(
            'name',
            'owner_name',
            'address',
            'city',
            'state',
            'veg',
            'image',
            'delivery_time',
            'mode_of_payment',
            'offer',
            'cuisines'
            )

class CustomerForm(forms.ModelForm):
    city=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    state=forms.ChoiceField(choices=[CHOICES], required=True,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    about=forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control',}))
    class Meta:
        model=UserProfile
        fields=('image','city','state','about','location')
        
