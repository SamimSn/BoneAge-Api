from rest_framework import serializers
from .models import BoneImage
from .utils import predict
from PIL import Image


class BoneImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoneImage
        fields = "__all__"
        extra_kwargs = {
            "result": {"read_only": True}
        }

    
    
