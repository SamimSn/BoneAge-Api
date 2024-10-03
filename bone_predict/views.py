from rest_framework.viewsets import ModelViewSet
import rest_framework.permissions as permissions
from .models import BoneImage
from .serializers import BoneImageSerializer
from .utils import predict


class BoneImageViewset(ModelViewSet):
    queryset = BoneImage.objects.all()
    serializer_class = BoneImageSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def perform_create(self, serializer):
            bone_image: BoneImage = serializer.save()
            bone_image.result = predict(str(bone_image.image))
            bone_image.save()