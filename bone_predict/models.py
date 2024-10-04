import uuid
from django.db import models


class BoneImage(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to="media/bone_images/")
    result = models.FloatField(null=True, blank=True)
