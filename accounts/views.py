from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        return render(request, 'accounts/register.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = AuthenticationForm


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
