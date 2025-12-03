from django.contrib import admin
from .models import Topf, Kostenstelle, Beschluss, Ausgabe


@admin.register(Topf)
class TopfAdmin(admin.ModelAdmin):
	list_display = ("name", "betrag")
	search_fields = ("name",)
	ordering = ("name",)


@admin.register(Kostenstelle)
class KostenstelleAdmin(admin.ModelAdmin):
	list_display = ("name", "betrag", "groupe", "topf")
	list_filter = ("topf", "groupe")
	search_fields = ("name",)
	ordering = ("name",)


@admin.register(Beschluss)
class BeschlussAdmin(admin.ModelAdmin):
	list_display = ("nummer", "name", "kommentar", "betrag", "kostenstelle", "beschluss_datum", "ablauf_datum")
	list_filter = ("kostenstelle", "beschluss_datum")
	search_fields = ("name", "nummer")
	ordering = ("-beschluss_datum",)


@admin.register(Ausgabe)
class AusgabeAdmin(admin.ModelAdmin):
	list_display = ("name", "kommentar", "betrag", "beschluss", "datum")
	list_filter = ("datum",)
	search_fields = ("name",)
	ordering = ("-datum",)

