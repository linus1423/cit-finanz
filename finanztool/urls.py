from django.urls import path
from .views import (
    home,
    BeschlussListView,
    BeschlussCreateView,
    BeschlussDetailView,
    AusgabeListView,
    AusgabeCreateView,
    AusgabeDetailView,
    TopfListView,
    TopfDetailView,
    KostenstelleListView,
    KostenstelleDetailView,
)

app_name = 'finanztool'

urlpatterns = [
    path('', home, name='home'),
    path('beschlusse/', BeschlussListView.as_view(), name='beschluss_list'),
    path('beschlusse/new/', BeschlussCreateView.as_view(), name='beschluss_create'),
    path('beschlusse/<int:pk>/', BeschlussDetailView.as_view(), name='beschluss_detail'),
    path('ausgaben/', AusgabeListView.as_view(), name='ausgabe_list'),
    path('ausgaben/new/', AusgabeCreateView.as_view(), name='ausgabe_create'),
    path('ausgaben/<int:pk>/', AusgabeDetailView.as_view(), name='ausgabe_detail'),
    path('topfe/', TopfListView.as_view(), name='topf_list'),
    path('topfe/<int:pk>/', TopfDetailView.as_view(), name='topf_detail'),
    path('kostenstellen/', KostenstelleListView.as_view(), name='kostenstelle_list'),
    path('kostenstellen/<int:pk>/', KostenstelleDetailView.as_view(), name='kostenstelle_detail'),
]