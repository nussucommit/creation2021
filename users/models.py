from django.db import models
from django.conf import settings
from django.utils.timezone import now
import pytz

# Create your models here.
class Image(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='img')
    img_url = models.CharField(max_length=300, blank = True)
    raw = models.FileField(upload_to='img')
    raw_url = models.CharField(max_length=300, blank = True)
    time = models.DateTimeField(default=now())
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    