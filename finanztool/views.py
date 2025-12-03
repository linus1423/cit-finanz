from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from .models import Topf, Kostenstelle, Beschluss, Ausgabe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TopfForm, KostenstelleForm, BeschlussForm, AusgabeForm
from datetime import date


class LoginRequiredBase(LoginRequiredMixin):
    """App-local base mixin for login-required views.

    Provides per-app defaults while still falling back to the global
    `LOGIN_URL` in settings if not overridden here.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


class BeschlussListView(LoginRequiredBase, ListView):
    model = Beschluss
    template_name = "beschluss-list.html"
    context_object_name = "beschlusse"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['today'] = date.today()
        return ctx


class BeschlussCreateView(LoginRequiredBase, CreateView):
    model = Beschluss
    form_class = BeschlussForm
    template_name = "beschluss-form.html"
    context_object_name = "beschlusse"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class BeschlussDetailView(LoginRequiredBase, DetailView):
    model = Beschluss
    template_name = "beschluss-detail.html"
    context_object_name = "beschluss"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['today'] = date.today()
        return ctx


class AusgabeListView(LoginRequiredBase, ListView):
    model = Ausgabe
    template_name = "ausgabe-list.html"
    context_object_name = "ausgaben"


class AusgabeCreateView(LoginRequiredBase, CreateView):
    model = Ausgabe
    form_class = AusgabeForm
    template_name = "ausgabe-form.html"
    context_object_name = "ausgaben"


class AusgabeDetailView(LoginRequiredBase, DetailView):
    model = Ausgabe
    template_name = "ausgabe-detail.html"
    context_object_name = "ausgabe"


class TopfListView(LoginRequiredBase, ListView):
    model = Topf
    template_name = "topf-list.html"
    context_object_name = "topfe"


class TopfDetailView(LoginRequiredBase, DetailView):
    model = Topf
    template_name = "topf-detail.html"
    context_object_name = "topf"


class KostenstelleListView(LoginRequiredBase, ListView):
    model = Kostenstelle
    template_name = "kostenstelle-list.html"
    context_object_name = "kostenstellen"


class KostenstelleDetailView(LoginRequiredBase, DetailView):
    model = Kostenstelle
    template_name = "kostenstelle-detail.html"
    context_object_name = "kostenstelle"


@login_required
def home(request):
    return render(request, 'home.html')



