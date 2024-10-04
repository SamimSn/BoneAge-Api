from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BoneImageViewset

router = DefaultRouter()

router.register(r"", BoneImageViewset, basename="bone-predict")

urlpatterns = [path("", include(router.urls))]
