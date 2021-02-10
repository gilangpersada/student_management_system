import json
import requests
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from smsApp.emailBackEnd import emailBackEnd

def showLogin(request):
    return render(request, 'login.html')

def userLogin(request):
    if request.method != 'POST':
        return HttpResponse('<h2>Not Allowed!</h2>')
    else:
        captcha_token = request.POST.get('g-recaptcha-response')
        cap_url = 'https://www.google.com/recaptcha/api/siteverify'
        cap_secret = '6LefoyIaAAAAAI0wkWs2QJTIO7AKtHtIWwZ8W7db'
        cap_data = {
            'secret': cap_secret,
            'response': captcha_token
        }
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)
        if cap_json['success'] == False:
            messages.error(request, 'Invalid captcha')
            return HttpResponseRedirect('/')

        email = request.POST.get('email')
        password = request.POST.get('password')
        user = emailBackEnd.authenticate(request, username=email, password=password)

        if user != None:
            login(request, user)
            if user.user_type == '1':
                return HttpResponseRedirect(reverse('admin_dashboard'))
            elif user.user_type == '2':
                return HttpResponseRedirect(reverse('staff_dashboard'))
            else:
                return HttpResponseRedirect(reverse('student_dashboard'))
        else:
            messages.error(request, 'Invalid login')
            return HttpResponseRedirect('/')

def getUserDetail(request):
    if request.user != None:
        user = request.user.email
        user_type = request.user.user_type
        return HttpResponse('User: ' + user + 'User Type: ' + user_type)
    else:
        return HttpResponse('Please login first!')

def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/')
