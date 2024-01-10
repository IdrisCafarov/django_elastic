from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from .forms import *

import random
import string


def code_slug_generator(size=12, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def create_slug_shortcode(size, model_):
    new_code = code_slug_generator(size=size)
    qs_exists = model_.objects.filter(slug=new_code).exists()
    return create_slug_shortcode(size, model_) if qs_exists else new_code


# Create your views here.


def user_login(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == 'POST':
        print("post")
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            print("valid")
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            login(request, user)
            # request.session.set_expiry(2000)

            return redirect('index')

    else:
        form = LoginForm()
    context["form"] = form
    return render(request,"login.html",context)



def logout_view(request):

    logout(request)
    return redirect('user_login')