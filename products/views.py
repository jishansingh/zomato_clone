from django.shortcuts import render,get_object_or_404,get_list_or_404
from .models import UserProfile,Restraunt,Review,Menu
from .forms import  AddRestraunt,CustomerForm
from .choices import CHOICES
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.shortcuts import redirect
# Create your views here.
def index(request):
    choice=[]
    for one in CHOICES:
        city={one[1]:one[0],}
        choice.append(city)
    context={'state':choice}
    print(choice)
    return render(request,'products/home.html',context)
    
def restraunt_all(request,state):
    res=get_list_or_404(Restraunt,state=state)
    context={'restraunt':res}
    return render(request,'products/restraunt.html',context)
def restraunt_city(request,state,city):
    res=get_list_or_404(Restraunt,state=state,city=city)
    context={'restraunt':res}
    return render(request,'products/restraunt_city.html',context)


def restraunt_detail(request,state,city,id):
    restraunt=get_object_or_404(Restraunt,pk=id,state=state,city=city)
    context={'restraunt':restraunt,'menu':restraunt.menu.all()}
    return render(request,'products/restraunt_detail.html',context)
def add_restraunt(request):
    if request.method=='POST':
        form=AddRestraunt(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    form=AddRestraunt()
    context={'form':form}
    return render(request,'products/add_restraunt.html',context)
def ProfileCreate(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        profile_form=ProfileForm(request.POST,request.FILES)
        if form.is_valid() and profile_form.is_valid():
            form=form.save(commit=False)
            user=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            form.save()
            new_user=authenticate(username=username,password=password)
            if new_user:
                profile_form=profile_form.save(commit=False)
                profile_form.user=new_user
                profile_form.save()
                login(request,new_user)
                return redirect('index')
    form=UserCreationForm()
    profile_form=CustomerForm()
    context={'form':form,'profile':profile_form}
    return render(request,'products/add_user.html',context)

