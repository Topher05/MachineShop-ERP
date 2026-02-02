from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'equipment', views.EquipmentViewSet, basename='equipment')
router.register(r'inspections', views.InspectionReportViewSet, basename='inspection')
router.register(r'characteristics', views.InspectionCharacteristicViewSet, basename='characteristic')

urlpatterns = [
    path('', include(router.urls)),
]