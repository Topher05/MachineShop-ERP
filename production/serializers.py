# production/serializer.py
from rest_framework import serializers
from .models import Customer, Contact, Quote, QuoteLineItem, Job, Operation

class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
	customer_name = serializers.CharField(source='customer.name', read_only=True)

	class Meta:
		model = Contact
		fields = '__all__'

class OperationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Operation
		fields = '__all__'

class JobDetailSerializer(serializers.ModelSerializer):
	operations = OperationSerializer(many=True, read_only=True)

	customer_name = serializers.CharField(source='customer.name', read_only=True)

	class Meta:
		model = Job
		fields = '__all__'

class JobListSerializer(serializers.ModelSerializer):
	customer_name = serializers.CharField(source='customer.name', read_only=True)

	class Meta:
		model = Job
		fields = '__all__'

class QuoteLineItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuoteLineItem
		fields = '__all__'

class QuoteDetailSerializer(serializers.ModelSerializer):
	line_items = QuoteLineItemSerializer(many=True, read_only=True)
	customer_name = serializers.CharField(source='customer.name', read_only=True)

	class Meta:
		model = Quote
		fields = '__all__'

class QuoteListSerializer(serializers.ModelSerializer):
	customer_name = serializers.CharField(source='customer.name', read_only=True)

	class Meta:
		model = Quote
		fields = ['id', 'quote_number', 'customer', 'customer_name', 
                  'status', 'total', 'created_at', 'valid_until']

