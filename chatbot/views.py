from django.shortcuts import render, redirect
from django.http import JsonResponse
import google.generativeai as genai

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone

genai.configure(api_key="")

prompt=["""
        You are a chatbot expert in answering any user questions!\n
        The user will ask questions, and you need to answer them!\n
        Also, the answers should not have ''' in the beginning or end in output.\n
        the programing language code should not have ''' in beginning or end .\n
"""]

def ask_gemini(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

def home(request):
    if request.user.is_authenticated:
        return redirect('chatbot')
    else:
        return redirect('login')

def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_gemini(message, prompt)
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth_login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Passwords dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth_logout(request)
    return redirect('login')
