from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from app.models import *
from django.contrib.auth.decorators import login_required


def registration(request):


    ufo=UserForm()
    pfo=ProfileForm()
    
    d={'ufo':ufo , 'pfo':pfo}

    if request.method == 'POST' and request.FILES:
        ufd = UserForm(request.POST)
        pfd = ProfileForm(request.POST , request.FILES)

        if ufd.is_valid() and pfd.is_valid():
            MUFDO = ufd.save(commit=False)
            pw = ufd.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()

            MPFDO = pfd.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save() 


            send_mail('Registration',
            'Registered Sucessfully',
            'suaraabinash1@gmail.com',
            [MUFDO.email],
            fail_silently=False)

            return HttpResponse("Registration done Sucessfully")

        else:
            return HttpResponse("invalid Data")
   
    return render(request,'registration.html',d)


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)

        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('credentials are not matching')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))