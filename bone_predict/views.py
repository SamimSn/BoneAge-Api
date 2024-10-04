from rest_framework.viewsets import ModelViewSet
from .models import BoneImage
from .serializers import BoneImageSerializer
from .utils import predict_in_thread


class BoneImageViewset(ModelViewSet):
    queryset = BoneImage.objects.all()
    serializer_class = BoneImageSerializer
    lookup_field = "uuid"

    def perform_create(self, serializer):
        bone_image: BoneImage = serializer.save()
        bone_image.result = predict_in_thread(str(bone_image.image))
        bone_image.save()
