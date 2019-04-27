from django.shortcuts import render,get_object_or_404,get_list_or_404
from .models import UserProfile,Restraunt,Review,Menu,new_request,Delivery,order_detail
from .forms import  AddRestraunt,CustomerForm,AddMenu,ReviewForm,ValetForm,LoginForm
from .choices import CHOICES
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.shortcuts import redirect
from django.http import Http404,HttpResponse
from django.contrib.auth import logout
# Create your views here.
def logout_user(request):
    logout(request)
    return redirect('index')
def index(request):
    choice=[]
    for one in CHOICES:
        city={one[1]:one[0],}
        choice.append(city)
    context={'state':choice}
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
    if request.method=='POST':
        form=ReviewForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.user=request.user
            form.save()
            review=restraunt.review
            review.add(form)
            restraunt.save()
    form=ReviewForm()
    context={'restraunt':restraunt,'menu':restraunt.menu.all(),'form':form}
    return render(request,'products/restraunt_detail.html',context)
def add_restraunt(request):
    if request.user.is_authenticated:
        profile=request.user.user_profile
        if not profile.customer:
            if request.method=='POST':
                form=AddRestraunt(request.POST,request.FILES)
                if form.is_valid():
                    form=form.save()
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
        if form.is_valid() and profile_form.is_valid():
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

def list_restraunt(request,id=0):
    if request.user.is_authenticated:
        profile=request.user.user_profile
        if not profile.customer:
            my=profile.my_restraunts.all()
            if request.method=='POST':
                restraunt=get_object_or_404(Restraunt,id=id)
                if restraunt in my:
                    pass
                else:
                    raise Http404()
                form=AddMenu(request.POST,request.FILES)
                if form.is_valid():
                    form=form.save()
                    restraunt.menu.add(form)
                    restraunt.save()
            form=AddMenu()
            context={'restraunt':my,'form':form}
            return render(request,'products/list_restraunt.html',context)
    raise Http404()

def edit_menu(request,id):
    if request.user.is_authenticated:
        profile=request.user.user_profile
        if not profile.customer:
            menu=get_object_or_404(Menu,id=id)
            my_res=profile.my_restraunts.all()
            flag=0
            for restraunt in my_res:
                if menu in restraunt.menu.all():
                    flag=1
            if flag is 0:
                raise Http404()
            if request.method=='POST':
                form=AddMenu(request.POST,request.FILES,instance=menu)
                if form.is_valid():
                    form.save()
                    return redirect('list_restraunt',id=0)
            form=AddMenu(instance=menu)
            context={'form':form,'id':id}
            return render(request,'products/addmenu.html',context)
    raise Http404()

def add_to_cart(request,id,pk,state,city):
    if request.user.is_authenticated:
        restraunt=get_object_or_404(Restraunt,id=id)
        menu=get_object_or_404(Menu,pk=pk)
        profile=request.user.user_profile
        cart=profile.cart
        cart.add(menu)
        fav=profile.fav_restraunts
        fav.add(restraunt)
        profile.save()
        return redirect('restraunt_detail',state=state,city=city ,id=id)
    raise Http404()

def profile(request):
    if request.user.is_authenticated:
        profile=request.user.user_profile
        context={'profile':profile,}
        return render(request,'products/profile.html',context)
def cart(request):
    profile=request.user.user_profile
    cart=profile.cart.all()
    context={'cart':cart,}
    return render(request,'products/cart.html',context)
def order_food(request,pk,id=-1):
    if request.user.is_authenticated:
        if id is -1:
            menu=get_object_or_404(Menu,pk=pk)
            restraunt=get_object_or_404(Restraunt,menu=menu)
        else:
            menu=get_object_or_404(Menu,pk=pk)
            restraunt=get_object_or_404(Restraunt,id=id)
        
        profile=request.user.user_profile
        valet=Delivery.objects.filter(is_available=True)
        if valet:
            valet=valet[0]
            new=order_detail(restraunt=restraunt,menu=menu,user_profile=profile)
            new.save()
            valet.is_available=False
            new_order=valet.order
            new_order.add(new)
            valet.save()
            context={'valet':valet,'orders':valet.order.all()}
            return render(request,'products/order.html',context)
        else:
            return HttpResponse('<h1>no delivery person is available at moment</h1>')
def valet_register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        profile_form=ValetForm(request.POST)
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
                return redirect('valet_login')
    form=UserCreationForm()
    profile_form=ValetForm()
    context={'form':form,'profile':profile_form}
    return render(request,'valet/valet_register.html',context)
def valet_login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return order_delivery(request)
    form=LoginForm()
    context={'form':form,}
    return render(request,'valet/valet_login.html',context)
def order_delivery(request):
    if request.user.is_authenticated:
        valet=get_object_or_404(Delivery,user=request.user)
        context={'valet':valet,'orders':valet.order.all()}
        return render(request,'valet/order_details.html',context)
def delivered(request,pk):
    order=get_object_or_404(order_detail,id=pk)
    order.delete()
    valet=get_object_or_404(Delivery,user=request.user)
    valet.is_available=True
    valet.save()
    return order_delivery(request)
def customer_login(request):
    if request.user.is_authenticated:
        raise Http404()
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('profile')
    form=LoginForm()
    context={'form':form,}
    return render(request,'products/login.html',context)
def show(request):
    if request.user.is_superuser:
        all=new_request.objects.all().order_by('approved')
        context={'all':all}
        return render(request,'products/request.html',context)
    raise Http404()
def approve(request,id):
    if request.user.is_superuser:
        req=get_object_or_404(new_request,id=id)
        req.approved=True
        user_profile=req.user.user_profile
        user_profile.customer=False
        user_profile.save()
        req.save()
        return show(request)
    raise Http404()
