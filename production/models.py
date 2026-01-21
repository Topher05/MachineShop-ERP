#production/models.py
from django.db import models

class Customer(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()

	def __str__(self):
		return self.name
	
class Job(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	job_number = models.CharField(max_length=50, unique=True)
	part_number = models.CharField(max_length=50)
	quantity = models.IntegerField()
	due_date = models.DateField()

	STATUS_CHOICES = [
		('QUOTE', 'Quoting'),
		('SCHEDULED', 'Scheduled'),
		('IN_PROCESS', 'In Process'),
		('COMPLETE', 'Complete'),
	]

	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='QUOTE')

	def __str__(self):
		return f"{self.job_number} - {self.customer.name}"

class Operation(models.Model):
	job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="operations")
	name = models.CharField(max_length=100, help_text="e.g., CNC Mill Op 1")
	estimated_hours = models.DecimalField(max_digits=5, decimal_places=2)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)

	class Meta:
		ordering=['start_date']