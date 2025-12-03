from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import date

class Topf(models.Model):
    name = models.CharField(max_length=50, unique=True)
    betrag = models.IntegerField()
       

    class Meta:
        verbose_name = _("Topf")
        verbose_name_plural = _("Töpfe")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("finanztool:topf_detail", kwargs={"pk": self.pk})

    def get_ausgegeben(self):
        return self.kostenstelle_set.aggregate(total=models.Sum('beschluss__ausgabe__betrag'))['total'] or 0

    def get_gebunden(self):
        total_kostenstelle = self.kostenstelle_set.aggregate(total=models.Sum('beschluss__betrag'))['total'] or 0
        ausgegeben = self.get_ausgegeben()
        return total_kostenstelle - ausgegeben
    
    def get_frei(self):
        total_kostenstelle = self.kostenstelle_set.aggregate(total=models.Sum('beschluss__betrag'))['total'] or 0
        gebunden = self.get_gebunden()
        return total_kostenstelle - gebunden

class Kostenstelle(models.Model):
    name = models.CharField(max_length=50, unique=True)
    betrag = models.IntegerField()
    groupe = models.ForeignKey('auth.Group', on_delete=models.PROTECT)
    topf = models.ForeignKey(Topf, on_delete=models.PROTECT)
    

    class Meta:
        verbose_name = _("Kostenstelle")
        verbose_name_plural = _("Kostenstellen")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("finanztool:kostenstelle_detail", kwargs={"pk": self.pk})
    
    def get_ausgegeben(self):
            return self.beschluss_set.aggregate(total=models.Sum('ausgabe__betrag'))['total'] or 0
    
    def get_gebunden(self):
        total_beschluss = self.beschluss_set.aggregate(total=models.Sum('betrag'))['total'] or 0
        ausgegeben = self.get_ausgegeben()
        return total_beschluss - ausgegeben
    
    def get_frei(self):
        total_beschluss = self.beschluss_set.aggregate(total=models.Sum('betrag'))['total'] or 0
        gebunden = self.get_gebunden()
        return total_beschluss - gebunden


class Beschluss(models.Model):
    nummer = models.IntegerField(unique=True)
    name = models.CharField(max_length=50, unique=True)
    kommentar = models.TextField(blank=True, null=True)
    betrag = models.IntegerField()
    kostenstelle = models.ForeignKey(Kostenstelle, on_delete=models.PROTECT)
    beschluss_datum = models.DateField()
    ablauf_datum = models.DateField()
    abgeschlossen = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Beschluss")
        verbose_name_plural = _("Beschlüsse")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("finanztool:beschluss_detail", kwargs={"pk": self.pk})

    @property
    def is_abgeschlossen(self):
        return self.abgeschlossen or self.ablauf_datum < date.today()

    def get_ausgegeben(self):
        return self.ausgabe_set.aggregate(total=models.Sum('betrag'))['total'] or 0

    def get_gebunden(self):
        if self.is_abgeschlossen():
            return 0
        else:
            return self.betrag - self.get_ausgegeben()

    def get_frei(self):
        if self.is_abgeschlossen():
            return 0
        else:
            return self.betrag - self.get_gebunden()

class Ausgabe(models.Model):
    name = models.CharField(max_length=50, unique=True)
    kommentar = models.TextField(blank=True, null=True)
    betrag = models.IntegerField()
    beschluss = models.ForeignKey(Beschluss, on_delete=models.PROTECT)
    datum = models.DateField()
    beleg = models.FileField(upload_to='belege/', null=True, blank=True)
    

    class Meta:
        verbose_name = _("Ausgabe")
        verbose_name_plural = _("Ausgaben")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("finanztool:ausgabe_detail", kwargs={"pk": self.pk})
