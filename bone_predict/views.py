from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .serializers import BoneImageSerializer
from .utils import predict_in_thread


class BoneImageViewset(ModelViewSet):
    queryset = (
        Profile.objects.all().filter(is_deleted=False).order_by("-created_at")
    )
    serializer_class = BoneImageSerializer
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance.result = predict_in_thread(instance.image_raw)
        instance.save()
        response_data = {
            "uuid": serializer.instance.uuid,
            "image_raw": request.build_absolute_uri(
                serializer.instance.image_raw.url
            ),
        }
        headers = self.get_success_headers(serializer.data)
        return Response(
            response_data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
