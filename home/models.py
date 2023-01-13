import uuid

from django.db import models

# Create your models here.


class Routers(models.Model):
    serialnumber = models.CharField(max_length=255, primary_key=True)
    username = models.CharField(max_length=255)
    routername = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    enterprise = models.CharField(max_length=255)
    ipaddress = models.GenericIPAddressField()

    def __str__(self):
        return "Le routeur {}:{} appartient à {}".format(self.routername, self.serialnumber, self.enterprise)


class Logs(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.TimeField()
    topics = models.CharField(max_length=300)
    message = models.TextField()
    router = models.ForeignKey(Routers, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-time']