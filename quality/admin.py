from django.contrib import admin

from .models import Equipment, InspectionReport, InspectionCharacteristic

admin.site.register(Equipment)

# This lets you edit characteristics INSIDE the Report page
class CharacteristicInline(admin.TabularInline):
    model = InspectionCharacteristic
    extra = 5 # Show 5 blank rows for data entry

@admin.register(InspectionReport)
class ReportAdmin(admin.ModelAdmin):
    inlines = [CharacteristicInline]
    list_display = ('fai_report_number', 'part_number', 'status', 'created_at')