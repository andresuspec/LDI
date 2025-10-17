from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import LoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Credenciales incorrectas.')

    return render(request, 'users/login.html', {'form': form})
