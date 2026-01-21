from django.contrib import admin
from .models import Customer, Job, Operation

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ('name', 'email')
	search_fields = ('name', 'email')

class OperationInline(admin.TabularInline):
	model = Operation
	extra = 1

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
	# This connects the Operations list to the Job page
	inlines = [OperationInline]
	
	# COLUMNS: What creates the table columns on the main list page
	list_display = ('job_number', 'customer', 'part_number', 'status', 'due_date')

	# FILTERS: Adds a sidebar to filter by Status or Customer
	list_filter = ('status', 'customer', 'due_date')

	# SEARCH: Adds a search bar at the top
	search_fields = ('job_number', 'part_number', 'customer__name')

	# ORDERING: Default sort order (newest due date first)
	ordering = ('due_date',)