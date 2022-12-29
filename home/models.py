import uuid

from django.db import models

# Create your models here.


class Routers(models.Model):
    SerialNumber = models.CharField(max_length=255, primary_key=True)
    Username = models.CharField(max_length=255)
    RouterName = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)
    Enterprise = models.CharField(max_length=255)


class Interface(models.Model):
    InterfaceID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    Type = models.CharField(max_length=255)
    IpAddress = models.GenericIPAddressField()
    RouterID = models.ForeignKey(Routers, on_delete=models.CASCADE)


class Logs(models.Model):
    LogID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.TimeField()
    topics = models.CharField(max_length=300)
    message = models.TextField()
    RouterID = models.ForeignKey(Routers, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-time']