from multiprocessing import context
from django.shortcuts import render,redirect

from stores.models import Order

from .forms import Createuser,Editprofile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate


from django.contrib import messages
# Create your views here.

def loginuser(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username'].lower()
            password = request.POST['pwd']

            try:
                user = User.objects.get(username = username)
            except:
                messages.error(request, 'Username Does Not exist!')
            user = authenticate(request, username = username,password = password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Username or Password Not Match!')
                return redirect('login')
    return render(request, 'users/login.html')

def register(request):
    form = Createuser()
    if request.method == 'POST':
        form = Createuser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            if User.objects.filter(email = user.email).exists():
                messages.error(request, 'Email Already Exist!')
                return redirect('register')
            user.save()
            
            messages.success(request, 'User Register Successfully!')
            login(request, user)
            return redirect('dashboard')
           
        else:
            messages.warning(request, 'User Register Failed!' )
    
    context={
        'form':form
    }

    return render(request, 'users/registration.html',context)


@login_required(login_url='login')
def dashboard(request):
    profile = request.user.profile
    order = Order.objects.filter(user=request.user, ordered=False)

    context={
        'profile':profile,
        'order':order
    }
    return render(request, 'users/dashboard.html',context)


def editprofile(request):
    profile = request.user.profile
    form = Editprofile(instance=profile)
    if request.method == 'POST':
        form = Editprofile(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    
    context = {
        'form':form
    }
    return render(request, 'users/editprofile.html',context)







def logoutuser(request):
    logout(request)
    messages.success(request, 'User Logged Out Successfully')
    return redirect('login')