from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import RedirectView, CreateView

from app.config import settings
from app.ecommerce.models import Categoria, Producto
from app.login.forms import UserCreationForm


class LoginFormView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        return context


class LogoutView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        return context


class UserCreationView(CreateView):
    form_class = UserCreationForm
    template_name = 'create.html'
    success_url = reverse_lazy('login')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Usuario'
        context['entity'] = 'Iniciar Sesión'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        return context
