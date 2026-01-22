from django.core.management.base import BaseCommand
from production.models import Customer, Contact, Job, Operation, Quote, QuoteLineItem
from quality.models import Equipment, InspectionReport, InspectionCharacteristic
from django.utils import timezone
import random
from datetime import timedelta, date

class Command(BaseCommand):
    help = 'Loads realistic aerospace demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write("--- Cleaning Old Data ---")
        InspectionCharacteristic.objects.all().delete()
        InspectionReport.objects.all().delete()
        Equipment.objects.all().delete()
        Operation.objects.all().delete()
        Job.objects.all().delete()
        QuoteLineItem.objects.all().delete()
        Quote.objects.all().delete()
        Contact.objects.all().delete()
        Customer.objects.all().delete()

        self.stdout.write("--- Creating Customers & Contacts ---")
        # 1. Boeing
        c1 = Customer.objects.create(
            name="Boeing Defense", 
            identification_prefix="BOE", 
            email="procurement@boeing.com",
            company_name="The Boeing Company",
            billing_address="100 N Riverside, Chicago, IL"
        )
        Contact.objects.create(customer=c1, first_name="Sarah", last_name="Connor", email="s.connor@boeing.com", title="Procurement Lead", is_key_contact=True)

        # 2. SpaceX
        c2 = Customer.objects.create(
            name="SpaceX", 
            identification_prefix="SPX", 
            email="starship.supply@spacex.com",
            company_name="Space Exploration Technologies",
            billing_address="1 Rocket Rd, Hawthorne, CA"
        )
        Contact.objects.create(customer=c2, first_name="Elon", last_name="Musk", email="elon@spacex.com", title="CEO", is_key_contact=True)

        self.stdout.write("--- Creating Quotes with Line Items ---")
        # Quote for SpaceX
        q1 = Quote.objects.create(
            customer=c2,
            valid_until=date.today() + timedelta(days=30),
            status='PENDING',
            overhead_amount=500.00,
            profit_amount=1200.00
        )
        # Add items (This triggers the subtotal calculation)
        QuoteLineItem.objects.create(quote=q1, part_number="SPX-TUBE-001", description="Fuel Line, Titanium", quantity=10, unit_price=450.00)
        QuoteLineItem.objects.create(quote=q1, part_number="SPX-BOLT-HEX", description="M10 Hex Bolt, Inconel", quantity=50, unit_price=25.50)

        self.stdout.write("--- Creating Jobs & Operations ---")
        # Convert that quote to a job manually for demo
        j1 = Job.objects.create(
            customer=c2,
            job_number="SPX-24-1-001",
            part_number="SPX-TUBE-001",
            quantity=10,
            due_date=date.today() + timedelta(days=14),
            status='IN_PROCESS',
            priority='HIGH',
            source_quote=q1
        )
        Operation.objects.create(job=j1, name="Saw Cut", estimated_hours=1.5, start_date=date.today())
        Operation.objects.create(job=j1, name="CNC Lathe Op 1", estimated_hours=4.0)

        # A late job
        j2 = Job.objects.create(
            customer=c1,
            job_number="BOE-24-1-055",
            part_number="737-LANDING-PIN",
            quantity=5,
            due_date=date.today() - timedelta(days=5), # OVERDUE
            status='SCHEDULED',
            priority='URGENT'
        )

        self.stdout.write("--- Creating Quality Data ---")
        caliper = Equipment.objects.create(name="Mitutoyo 6in Caliper", serial_number="CAL-001", last_calibration_date=date.today() - timedelta(days=30))
        
        # FAI Report for the SpaceX Job
        fai = InspectionReport.objects.create(
            job=j1,
            inspection_type='FAI',
            part_number="SPX-TUBE-001",
            part_name="Fuel Line",
            fai_report_number="FAI-SPX-001",
            status='PENDING'
        )
        
        # Characteristics (Form 3)
        InspectionCharacteristic.objects.create(
            report=fai, char_number=1, description="Overall Length", requirement="10.000 +/- 0.005",
            nominal_value=10.000, upper_tolerance=0.005, lower_tolerance=0.005,
            actual_value=10.001, equipment_used=caliper
        )
        # A failing dimension
        InspectionCharacteristic.objects.create(
            report=fai, char_number=2, description="Outer Diameter", requirement="1.500 +/- 0.001",
            nominal_value=1.500, upper_tolerance=0.001, lower_tolerance=0.001,
            actual_value=1.504, equipment_used=caliper # This should auto-fail
        )

        self.stdout.write(self.style.SUCCESS("Successfully populated demo data!"))