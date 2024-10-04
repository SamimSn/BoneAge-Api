import mimetypes
from rest_framework import serializers
from .models import BoneImage


class BoneImageSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(write_only=True)

    class Meta:
        model = BoneImage
        fields = ["image_url", "result", "image"]

    def get_result(self, obj):
        total_months = obj.result
        years = int(total_months // 12)
        months = int(total_months % 12)
        return {
            "years": years,
            "months": months,
        }

    def get_image_url(self, obj):
        return f"https://hoomprovpn.info/{obj.uuid}"

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
