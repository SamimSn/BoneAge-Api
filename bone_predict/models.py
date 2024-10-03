from django.db import models


class BoneImage(models.Model):
    image = models.ImageField(upload_to="media/bone_images/")
    result = models.FloatField(null=True, blank=True)