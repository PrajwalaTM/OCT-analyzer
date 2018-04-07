from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ImageModel(models.Model):
   name = models.CharField(max_length=500,default='image')
   image = models.ImageField(upload_to = 'images/', null=True, verbose_name="")

   def __str__(self):
        return self.name + ": " + str(self.image)
