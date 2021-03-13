from django.shortcuts import render
from blog.models import UserProfileInfo
from blog.forms import UserForm, UserProfileInfoForm

#for login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

def index(request):
    dict={'name':"Josafat Corona"}
    return render(request,'index.html',context= dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("User is not active")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} password {}".format(username, password))
            return HttpResponse("Credentianls failed")
    else:
        return render(request,'blog/login.html',{})

def register(request):
    registered = False
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileInfoForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'blog/register.html',{
                                                'user_form':user_form,
                                                'profile_form':profile_form,
                                                'registered':registered})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
