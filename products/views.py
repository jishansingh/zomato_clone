from django.shortcuts import render,get_object_or_404,get_list_or_404
from .models import UserProfile,Restraunt,Review,Menu,new_request
from .forms import  AddRestraunt,CustomerForm,AddMenu
from .choices import CHOICES
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.shortcuts import redirect
from django.http import Http404
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
    if request.user.is_authenticated:
        profile=request.user.user_profile
        if not profile.customer:
            if request.method=='POST':
                form=AddRestraunt(request.POST,request.FILES)
                if form.is_valid():
                    form.save()
                    profile.my_restraunts.add(form)
                    profile.save()
            form=AddRestraunt()
            context={'form':form}
            return render(request,'products/add_restraunt.html',context)
    raise Http404()
def ProfileCreate(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        profile_form=CustomerForm(request.POST,request.FILES)
        if form.is_valid():
            form=form.save(commit=False)
            user=request.POST['username']
            password=request.POST['password1']
            form.save()
            new_user=authenticate(username=user,password=password)
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

def send_request(request):
    if request.user.is_authenticated:
        new=new_request.objects.filter(user=request.user)
        if new.exists():
            return HttpResponse('<h1>request in progress</h1>')
        else:
            new=new_request(user=request.user)
            new.save()
            return HttpResponse('<h1>request sent</h1>')
    raise Http404()
    
def edit_profile(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            profile=request.user.user_profile
            form=CustomerForm(request.POST,instance=profile)
            if form.is_valid():
                form.save()
        form=CustomerForm(instance=request.user.user_profile)
        context={'form':form}
        return render(request,'products/edit_profile.html',context)
    raise Http404()

def list_restraunt(request,id):
    if request.user.is_authenticated:
        profile=request.user.user_profile
        if not profile.customer:
            if request.method=='POST':
                restraunt=get_object_or_404(Restraunt,id=id)
                form=AddMenu(request.POST,request.FILES)
                if form.is_valid():
                    form.save()
                    restraunt.menu.add(form)
                    restraunt.save()
            my=profile.my_restraunts.all()
            form=AddMenu()
            context={'restraunt':my,'form':form}
            return render(request,'products/list_restraunt.html',context)
    raise Http404()

def edit_menu(request,id):
    if request.user.is_authenticated:
        profile=request.user.user_profile
        if not profile.customer:
            menu=get_object_or_404(Menu,id=id)
            if request.method=='POST':
                form=AddRestraunt(request.POST,request.FILES,instance=menu)
                if form.is_valid():
                    form.save()
            form=AddMenu(instance=menu)
            context={'form':form,'id':id}
            return render(request,'products/addmenu.html',context)
    raise Http404()
    