from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.
class LoginView(View):
    def get(selfself, request):
        template_name = "authentication_login.html"
        context = {}
        return render(request, template_name, context=context)

    def post(selfself, request):
        template_name = "authentication_login.html"
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Login success")
        else:
            context = {
                'error': "wrong credentials",
                'username': "username or password is not match",
                'password': "username or password is not match"
            }
            return render(request, template_name, context=context)