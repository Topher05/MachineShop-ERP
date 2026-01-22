#production/models.py
from django.db import models
from decimal import Decimal

class Customer(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	
	identification_prefix = models.CharField(
		max_length=10,
		unique=True,
		help_text="Used for quote/job numbering"
	)
	company_name = models.CharField(max_length=200, blank=True)
	billing_address = models.TextField(blank=True)
	phone = models.CharField(max_length=20, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name
	
class Contact(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	phone = models.CharField(max_length=20, blank=True)
	title = models.CharField(max_length=100, blank=True)

	is_key_contact = models.BooleanField(
		default=False,
		help_text="Main Contact for Company"
	)

	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-is_key_contact', 'last_name']
	
	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.customer.name})" 
	
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

	PRIORITY_CHOICES = [
		('LOW', 'Low'),
		('NORMAL', 'Normal'),
		('HIGH', 'High'),
		('URGENT', 'Urgent'),
	]

	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='QUOTE')
	priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='NORMAL')

	created_at = models.DateTimeField(auto_now_add=True)
	started_at = models.DateTimeField(null=True, blank=True)
	completed_at = models.DateTimeField(null=True, blank=True)

	notes = models.TextField(blank=True)

	source_quote = models.OneToOneField(
		'Quote',
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='job',
	)

	@property
	def is_overdue(self):
		from django.utils import timezone
		return self.due_date < timezone.now().date() and self.status != 'COMPLETED'

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

class QuoteCounter(models.Model):
    """Tracks sequential numbering per customer/year/quarter"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    year = models.IntegerField()
    quarter = models.IntegerField()
    count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['customer', 'year', 'quarter']
    
    def __str__(self):
        return f"{self.customer.identification_prefix} {self.year}Q{self.quarter}: {self.count}"

class Quote(models.Model):
	STATUS_CHOICES = [
		('PENDING', 'Pending'),
		('SENT', 'Sent'),
      ('ACCEPTED', 'Accepted'),
      ('REJECTED', 'Rejected'),
	]	

	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='quotes')
	quote_number = models.CharField(max_length=50, unique=True, editable=False)
	
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
	
	# Dates
	created_at = models.DateTimeField(auto_now_add=True)
	sent_at = models.DateTimeField(null=True, blank=True)
	valid_until = models.DateField(help_text="Quote expiration date")
	
	# Financial
	subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	overhead_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	profit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	
	# Notes
	notes = models.TextField(blank=True)

	def calculate_totals(self):
		lines = self.line_items.all()
		self.subtotal = sum(Decimal(str(line.total_price)) for line in lines)
		
		overhead = Decimal(str(self.overhead_amount))
		profit = Decimal(str(self.profit_amount))
		self.total = self.subtotal + overhead + profit
		
		super().save(update_fields=['subtotal', 'total'])

	def save(self, *args, **kwargs):
		if not self.quote_number:
			self.quote_number = self.generate_quote_number()
		super().save(*args, **kwargs)
	
	def generate_quote_number(self):
		from django.db import transaction
		from datetime import datetime 

		now = datetime.now()
		year = now.year % 100 # gets the last 2 digits
		quarter = (now.month - 1) // 3 + 1

		with transaction.atomic():
			counter, created = QuoteCounter.objects.select_for_update().get_or_create(
				customer = self.customer,
				year = year,
				quarter = quarter,
				defaults = {'count': 0}
			)
			counter.count += 1
			counter.save()

		return f"{self.customer.identification_prefix}{year}Q{quarter}-{counter.count:03d}"
	
class QuoteLineItem(models.Model):
    """Individual parts/items on a quote"""
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='line_items')
    
    part_number = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.IntegerField()
    
    # Costing breakdown
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    # Time estimates (for reference)
    setup_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    machining_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    programming_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
        # Recalculate quote totals
        self.quote.calculate_totals()
    
    def __str__(self):
        return f"{self.part_number} (Qty: {self.quantity})"	