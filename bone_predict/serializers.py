import mimetypes
from rest_framework import serializers
from .models import BoneImage


class BoneImageSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True)
    years = serializers.SerializerMethodField(read_only=True)
    months = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BoneImage
        fields = ["image_url", "years", "months", "image"]

    def get_years(self, obj):
        return int(obj.result // 12)

    def get_months(self, obj):
        return int(obj.result % 12)

    def get_image_url(self, obj):
        return f"https://hoomprovpn.info/media/bone_images/{obj.image.name}"

    def validate_image(self, value):
        # 1. Check file MIME type
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

        # 2. Check file size (5 MB = 5 * 1024 * 1024 bytes)
        max_size = 5 * 1024 * 1024  # 5 MB limit
        if value.size > max_size:
            raise serializers.ValidationError(
                f"File size must not exceed 5 MB. The uploaded file is {value.size / (1024 * 1024):.2f} MB."
            )

        return value
