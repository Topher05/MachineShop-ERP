# quality/models.py
from django.db import models
from django.utils import timezone

class Equipment(models.Model):
	name = models.CharField(max_length=100)
	serial_number = models.CharField(max_length=50)
	last_calibration_date = models.DateField()
	calibration_interval_days = models.IntegerField(default=365)

	def is_calibration_due(self):
		next_due = self.last_calibration_date + timezone.timedelta(days=self.calibration_interval_days)
		return next_due <= timezone.now().date()
	
	def __str__(self):
		return f"{self.name} - {self.serial_number}"
	
class InspectionReport(models.Model):
	part_number = models.CharField(max_length=50)
	part_name = models.CharField(max_length=100)
	serial_number = models.CharField(max_length=50, blank=True)
	fai_report_number = models.CharField(max_length=50, unique=True)
	created_at = models.DateField(auto_now_add=True)

	STATUS_CHOICES = [
		('PENDING', 'Pending'),
		('PASS', 'Pass'),
		('FAIL', 'Fail'),
	]

	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")

	def __str__(self):
		return f"FAI-{self.fai_report_number} ({self.part_number})"
	
class InspectionCharacteristic(models.Model):
    # This represents ONE line on AS9102 Form 3
    report = models.ForeignKey(InspectionReport, on_delete=models.CASCADE, related_name="characteristics")
    char_number = models.IntegerField(help_text="The balloon number from the drawing")
    
    description = models.CharField(max_length=200, help_text="e.g., Hole Diameter")
    requirement = models.CharField(max_length=100, help_text="e.g., 0.500 +/- 0.005")
    
    # Tolerances for calculation
    nominal_value = models.DecimalField(max_digits=10, decimal_places=4)
    upper_tolerance = models.DecimalField(max_digits=10, decimal_places=4)
    lower_tolerance = models.DecimalField(max_digits=10, decimal_places=4)
    
    # The Result
    actual_value = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    pass_fail = models.BooleanField(default=False)
    
    equipment_used = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-calculate Pass/Fail before saving
        if self.actual_value is not None:
            upper_limit = self.nominal_value + self.upper_tolerance
            lower_limit = self.nominal_value - self.lower_tolerance
            self.pass_fail = lower_limit <= self.actual_value <= upper_limit
        super().save(*args, **kwargs)