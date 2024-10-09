from rest_framework import serializers
from .models import Profile
from .services import bone_predict_service


class BoneImageSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "uuid",
            "created_at",
            "updated_at",
            "image_raw",
            "image_marked",
            "first_name",
            "last_name",
            "phone_number",
            "age",
            "result",
        ]

    def get_result(self, obj):
        result = obj.result
        if result:
            months = int(result) % 12
            years = int(result) // 12
            return {"year(s)": years, "month(s)": months}
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        if instance.image_raw:
            representation["image_raw"] = request.build_absolute_uri(
                instance.image_raw.url
            )
        if instance.image_marked:
            representation["image_marked"] = request.build_absolute_uri(
                instance.image_marked.url
            )
        return representation

    def validate_image_raw(self, value):
        bone_predict_service.validate_image_format(value)
        bone_predict_service.validate_image_size(value)
        bone_predict_service.validate_image(value)
        return value

    # def validate(self, attrs):
    #     view = self.context.get("view")
    #     bone_predict_service.validate(attrs, view)
    #     return attrs

    def get_fields(self):
        fields = super().get_fields()
        view = self.context.get("view")
        bone_predict_service.get_fields(fields, view)
        return fields
