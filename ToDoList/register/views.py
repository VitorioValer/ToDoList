from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib import messages


# Create your views here.
def register(response):
    if response.user.is_authenticated:
        return redirect('/login')

    else:
        if response.method == 'POST':
            form = RegisterForm(response.POST)

            if form.is_valid():
                user = form.save()
                
                login(response, user)
                messages.success(response, 'Registration successful.')

            
                return redirect('/')
            
            messages.error(response, 'Unseccessful registration. Please check the information!')
        
        form = RegisterForm()

        return render(response, 'register/register.html', {'form': form})
