from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Equipment, InspectionReport, InspectionCharacteristic
from .serializers import (
    EquipmentSerializer,
    InspectionReportListSerializer,
    InspectionReportDetailSerializer,
    InspectionCharacteristicSerializer
)

class EquipmentViewSet(viewsets.ModelViewSet):
	queryset = Equipment.objects.all()
	serializer_class = EquipmentSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['name', 'serial_number']

	@action(detail=False, methods=['get'])
	def calibration_due(self, request):
		due_equipment = [eq for eq in self.get_queryset() if eq.is_calibration_due()]
		serializer = EquipmentSerializer(due_equipment, many=True)
		return Response(serializer.data)
	
class InspectionReportViewSet(viewsets.ModelViewSet):
	queryset = InspectionReport.objects.prefetch_related('characteristics')
	filter_backends = [filters.SearchFilter, DjangoFilterBackend]
	search_fields = ['fai_report_number', 'part_number']
	filterset_fields = ['status', 'inspection_type']
	ordering = ['-created_at']

	def get_serializer_class(self):
		if self.action == 'list':
			return InspectionReportListSerializer
		return InspectionReportDetailSerializer
	
class InspectionCharacteristicViewSet(viewsets.ModelViewSet):
	queryset = InspectionCharacteristic.objects.all()
	serializer_class = InspectionCharacteristicSerializer
	filterset_fields = ['report', 'pass_fail']