from django.db import models

# Create your models here.


from django.db import models


class Image(models.Model):
    photo: models.ImageField = models.ImageField(upload_to="pics")
