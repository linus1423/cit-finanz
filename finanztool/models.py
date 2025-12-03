from django.db import models

class Topf(models.Model):
    name = models.CharField(max_length=50, )
    betrag = models.IntegerField()

    

    class Meta:
        verbose_name = _("Topf")
        verbose_name_plural = _("Topfs")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Topf_detail", kwargs={"pk": self.pk})

class Kostenstelle(models.Model):

    

    class Meta:
        verbose_name = _("kostenstelle")
        verbose_name_plural = _("kostenstelles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("kostenstelle_detail", kwargs={"pk": self.pk})


class Beschluss(models.Model):

    

    class Meta:
        verbose_name = _("Beschluss")
        verbose_name_plural = _("Beschlusss")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Beschluss_detail", kwargs={"pk": self.pk})

class Ausgabe(models.Model):

    

    class Meta:
        verbose_name = _("Ausgabe")
        verbose_name_plural = _("Ausgabes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Ausgabe_detail", kwargs={"pk": self.pk})
