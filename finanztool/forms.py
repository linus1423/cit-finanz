from django import forms
from django.core.exceptions import ValidationError
from .models import Topf, Kostenstelle, Beschluss, Ausgabe
from datetime import date


class TopfForm(forms.ModelForm):
    class Meta:
        model = Topf
        fields = ["name", "betrag"]
        widgets = {
            "betrag": forms.NumberInput(attrs={"min": 0}),
        }


class KostenstelleForm(forms.ModelForm):
    class Meta:
        model = Kostenstelle
        fields = ["name", "betrag", "groupe", "topf"]
        widgets = {
            "betrag": forms.NumberInput(attrs={"min": 0}),
        }


class BeschlussForm(forms.ModelForm):
    class Meta:
        model = Beschluss
        fields = [
            "nummer",
            "name",
            "betrag",
            "kostenstelle",
            "beschluss_datum",
            "ablauf_datum",
        ]
        widgets = {
            "betrag": forms.NumberInput(attrs={"min": 0}),
            "beschluss_datum": forms.DateInput(attrs={"type": "date"}),
            "ablauf_datum": forms.DateInput(attrs={"type": "date"}),
        }
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("beschluss_datum")
        end = cleaned.get("ablauf_datum")
        if start and end and end < start:
            self.add_error("ablauf_datum", "Ablaufdatum muss nach dem Beschlussdatum liegen.")

        kost = cleaned.get("kostenstelle")
        # If user was passed in, check that the Kostenstelle belongs to one of user's groups
        if self.user and kost:
            user_group = self.user.groups.first()
            if user_group and getattr(kost, 'groupe', None) != user_group:
                # raise a ValidationError mapped to the field so the form is marked invalid
                raise ValidationError({
                    "kostenstelle": "Die Kostenstelle gehört nicht zu Ihrer Gruppe."
                })
            if kost.groupe not in self.user.groups.all():
                raise ValidationError({'kostenstelle': "Die Kostenstelle gehört nicht zu Ihrer Gruppe."})

        return cleaned


class AusgabeForm(forms.ModelForm):
    class Meta:
        model = Ausgabe
        fields = ["name", "betrag", "beschluss", "datum", "beleg"]
        widgets = {
            "betrag": forms.NumberInput(attrs={"min": 0}),
            "datum": forms.DateInput(attrs={"type": "date"}),
            "beleg": forms.FileInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()
        self.fields['beschluss'].queryset = Beschluss.objects.filter(abgeschlossen=False, ablauf_datum__gte=today)

    def clean(self):
        cleaned = super().clean()
        beschluss = cleaned.get("beschluss")
        if beschluss:
            # Use the Beschluss.is_abgeschlossen property (safe if absent)
            if getattr(beschluss, "is_abgeschlossen", False):
                raise ValidationError({
                    "beschluss": "Dem Beschluss können keine Ausgaben mehr zugeordnet werden, da er abgeschlossen oder abgelaufen ist."
                })
        return cleaned
