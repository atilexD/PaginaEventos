from django.db import models
from django.dispatch import receiver

from uuid import uuid4
from time import strftime
import os.path

# Create your models here.

def imageName(instance, filename):
    if instance.id:
        eve = Evento.objects.get(pk=instance.id)
        os.remove(eve.URLImg.path)
    path = 'eventosImg/' + strftime('%Y/%m/%d/') + str(uuid4())
    path += os.path.splitext(filename)[1]
    return path

class Precio(models.Model):
    precio = models.DecimalField(max_digits=7, decimal_places=2,
                unique=True)

    def __unicode__(self):
        return unicode(self.precio)

class Hora(models.Model):
    hora = models.TimeField(unique=True)

    def __unicode__(self):
        return unicode(self.hora)

class Fecha(models.Model):
    fecha = models.DateField(unique=True)

    def __unicode__(self):
        return unicode(self.fecha)

class GeneroMusical(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.nombre

class Artista(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    generosmusicales = models.ManyToManyField(GeneroMusical,
            verbose_name='genero musical')

    def __unicode__(self):
        return unicode(self.nombre)

class TipoEvento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.nombre

class TipoObraTeatro(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.nombre

class TipoDanza(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.nombre

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    URLImg = models.ImageField(upload_to=imageName, verbose_name='imagen')
    URLWeb = models.URLField('pagina web')
    descripcion = models.TextField()
    fecHoraPub = models.DateTimeField(auto_now_add=True)
    nVisitas = models.IntegerField(default=0, editable=False)
    precios = models.ManyToManyField(Precio)
    horas = models.ManyToManyField(Hora)
    fechas = models.ManyToManyField(Fecha)
    tipoevento = models.ForeignKey(TipoEvento)
    artistas = models.ManyToManyField(Artista)
    establecimiento = models.ForeignKey('Establecimiento.Establecimiento')

    def __unicode__(self):
        return self.nombre

class EventoConcierto(models.Model):
    idEventoConcierto = models.ForeignKey(Evento, primary_key=True)
    generomusical = models.ForeignKey(GeneroMusical)

class EventoObraTeatro(models.Model):
    idEventoObraTeatro = models.ForeignKey(Evento, primary_key=True)
    tipoobrateatro = models.ForeignKey(TipoObraTeatro)

class EventoDanza(models.Model):
    idEventoDanza = models.ForeignKey(Evento, primary_key=True)
    tipodanza = models.ForeignKey(TipoDanza)

@receiver(models.signals.post_delete, sender=Evento)
def evento_post_delete(sender, instance, **kwargs):
    """Elimina archivos cuando un objeto de tipo Evento es eliminado."""
    if instance.URLImg:
        if os.path.isfile(instance.URLImg.path):
            os.remove(instance.URLImg.path)

