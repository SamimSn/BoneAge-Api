import os
import uuid
from django.db import models


class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=False)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    image_raw = models.ImageField(
        upload_to="images_raw/", null=False, blank=False
    )
    image_marked = models.ImageField(
        upload_to="images_marked/", null=True, blank=True
    )
    result = models.FloatField(null=True, blank=True)

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    def delete(self):
        self.is_deleted = True
        self.save()


class TemporaryImage(models.Model):
    image = models.ImageField(
        upload_to="images_temporary/", null=False, blank=False
    )

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)
