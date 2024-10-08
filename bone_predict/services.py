import mimetypes
from rest_framework import serializers
from django.conf import settings
from .utils import predict_is_image_valid_in_thread


class BonePredictService:
    def validate_image_format(self, value):
        valid_mime_types = [
            "image/jpeg",
            "image/jpg",
            "image/png",
            "image/bmp",
        ]
        file_mime_type, _ = mimetypes.guess_type(value.name)

        if file_mime_type not in valid_mime_types:
            raise serializers.ValidationError(
                "Unsupported file type. Only JPEG, PNG, JPG, and BMP files are allowed."
            )

    def validate_image_size(self, value):
        size = settings.IMAGE_SIZE
        if value.size > size:
            raise serializers.ValidationError(
                f"File size must not exceed {size} MB. The uploaded file is {value.size / (1024 * 1024):.2f} MB."
            )

    def validate_image(self, value):
        if not predict_is_image_valid_in_thread(value):
            raise serializers.ValidationError(
                "The uploaded image is invalid according to the model prediction."
            )

    def get_fields(self, fields, view):
        if fields.get("id"):
            fields.pop("id")

        if view and view.action == "create":
            allowed_fields = ["image_raw"]
            for field_name in list(fields.keys()):
                if field_name not in allowed_fields:
                    fields[field_name].read_only = True

        elif view and view.action in ["partial_update", "update"]:
            allowed_fields = [
                "first_name",
                "last_name",
                "phone_number",
                "age",
            ]
            for field_name in list(fields.keys()):
                if field_name not in allowed_fields:
                    fields[field_name].read_only = True

    def validate(self, attrs: dict, view):
        if view and view.action == "create":
            print(attrs)
            if len(attrs) != 1 or not attrs.get("image_raw"):
                raise serializers.ValidationError(
                    "Only 'image_raw' is allowed for creation."
                )
        if view and view.action in ["partial_update", "update"]:

            allowed_fields = [
                "first_name",
                "last_name",
                "phone_number",
                "age",
            ]

            for field in attrs:
                if field not in allowed_fields:
                    attrs.pop(field)


bone_predict_service = BonePredictService()
