# quality/serializers.py
from rest_framework import serializers
from .models import Equipment, InspectionReport, InspectionCharacteristic

class EquipmentSerializer(serializers.ModelSerializer):

	calibration_status = serializers.SerializerMethodField()

	class Meta:
		model = Equipment
		fields = '__all__'

	def get_calibration_status(self, obj):
		return "DUE" if obj.is_calibration_due() else "CURRENT"
	
class InspectionCharacteristicSerializer(serializers.ModelSerializer):
	equipment_name = serializers.CharField(
		source='equipment_used.name',
		read_only=True,
		allow_null=True
	)

	class Meta: 
		model = InspectionCharacteristic
		fields = '__all__'

class InspectionReportDetailSerializer(serializers.ModelSerializer):
	characteristics = InspectionCharacteristicSerializer(many=True, read_only=True)

	class Meta:
		model = InspectionCharacteristic
		fields = '__all__'

class InspectionReportDetailSerializer(serializers.ModelSerializer):
	characteristics = InspectionCharacteristicSerializer(many=True, read_only=True)

	class Meta:
		model = InspectionReport
		fields = '__all__'

class InspectionReportListSerializer(serializers.ModelSerializer):
	class Meta:
		model = InspectionReport
		fields = ['id', 'fai_report_number', 'part_number', 'part_name', 
                  'inspection_type', 'status', 'created_at', 'inspection_date']