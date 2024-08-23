from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

def registration(request):

    UF=UserForm()
    PF=ProfileForm()
    d={'UF':UF,'PF':PF}

    if request.method=='POST'and request.FILES:
        NMUFDO=UserForm(request.POST)
        NMPFDO=ProfileForm(request.POST,request.FILES)
        if NMUFDO.is_valid and NMPFDO.is_valid():
            MFUFDO=NMUFDO.save(commit=False)
            pw=NMUFDO.cleaned_data['password']
            MFUFDO.set_password(pw)
            MFUFDO.save() #This will save the user email


            MFPFDO=NMPFDO.save(commit=False)
            MFPFDO.username=MFUFDO
            MFPFDO.save()

            send_mail ('Registeration Process',
                      'Thank You Registration is Successfull!!!',
                      'rakeshmeher953@gmail.com',
                      [MFUFDO.email],
                      fail_silently=False)

            return HttpResponse('registration is successfull!!')
        else:
            return HttpResponse('Registration Unsuccessfull')
            
    return render(request,'registration.html',d)

def Home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'Home.html',d)
    return render(request,'Home.html')



def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('Home'))
        else:
            return HttpResponse('Invalid Credentials')
    return render(request,'user_login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Home'))


def display_data(request):
    un=request.session.get('username')
    UP=User.objects.get(username=un)
    PO=ProfilePic.objects.get(username=UP)
    d={'UP':UP,'PO':PO}
    return render(request,'display_data.html',d)