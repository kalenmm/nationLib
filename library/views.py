from django.shortcuts import render


def IndexView(request):
    template_name = "library/index.html"
    return render(request, template_name)


def LoginView(request):
    template_name = "library/login.html"
    return render(request, template_name)


def RegisterView(request):
    template_name = "library/register.html"
    return render(request, template_name)

