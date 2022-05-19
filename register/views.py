from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from register.forms import RegisterForm
# User = get_user_model()


def register(response):
    context = {}
    if response.POST:
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(response, user)
            return redirect('home')   # redirecting here
        else:
            context['registration_form'] = form
    else:
        form = RegisterForm()
        context['registration_form'] = form
    return render(response, 'register/register.html', context)
    # user = User.objects.get()
    # if response.method == "POST":
    #     form = RegisterForm(response.POST)
    #     if form.is_valid():
    #         form.save()
    #
    #     return redirect("/library")
    # else:
    #     form = RegisterForm()
    # return render(response, "register/register.html", {"form": form})
