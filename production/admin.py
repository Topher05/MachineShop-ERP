#production/admin.py
from django.contrib import admin
from .models import (
    Customer, Contact, Quote, QuoteLineItem, QuoteCounter,
    Job, Operation
)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'identification_prefix', 'email', 'is_active')
    search_fields = ('name', 'email', 'identification_prefix')
    list_filter = ('is_active',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'customer', 'email', 'is_key_contact')
    list_filter = ('is_key_contact', 'customer')
    search_fields = ('first_name', 'last_name', 'email')

class QuoteLineItemInline(admin.TabularInline):
    model = QuoteLineItem
    extra = 1
    readonly_fields = ('total_price',)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    inlines = [QuoteLineItemInline]
    list_display = ('quote_number', 'customer', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('quote_number', 'customer__name')
    readonly_fields = ('quote_number', 'subtotal', 'overhead_amount', 'profit_amount', 'total')

@admin.register(QuoteCounter)
class QuoteCounterAdmin(admin.ModelAdmin):
    list_display = ('customer', 'year', 'quarter', 'count')
    list_filter = ('year', 'quarter')

class OperationInline(admin.TabularInline):
    model = Operation
    extra = 1

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    inlines = [OperationInline]
    list_display = ('job_number', 'customer', 'part_number', 'status', 'priority', 'due_date', 'is_overdue')
    list_filter = ('status', 'priority', 'customer', 'due_date')
    search_fields = ('job_number', 'part_number', 'customer__name')
    ordering = ('due_date',)
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
