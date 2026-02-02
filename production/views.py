# production/views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Customer, Contact, Quote, Job, Operation
from .serializers import (
	CustomerSerializer,
	ContactSerializer,
	QuoteListSerializer,
	QuoteDetailSerializer,
	JobListSerializer,
	JobDetailSerializer,
	OperationSerializer
)

class CustomerViewSet(viewsets.ModelViewSet):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer

	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['name', 'email', 'identification_prefix']
	ordering_fields = ['name', 'created_at']
	ordering = ['name']

class ContactViewSet(viewsets.ModelViewSet):
	queryset = Contact.objects.all()
	serializer_class = ContactSerializer

	filter_backends = [filters.SearchFilter, DjangoFilterBackend]
	search_fields = ['first_name', 'last_name', 'email']
	filterset_fields = ['customer', 'is_key_contact']

class JobViewSet(viewsets.ModelViewSet):
	queryset = Job.objects.select_related('customer').prefetch_related('operations')
	filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
	search_fields = ['job_number', 'part_number']
	filterset_fields = ['status', 'priority', 'customer']
	ordering_fields = ['due_date', 'created_at', 'priority']
	ordering = ['due_date']

	def get_serializer_class(self):
		if self.action == 'list':
			return JobListSerializer
		return JobDetailSerializer
	
	@action(detail=False, methods=['get'])
	def overdue(self, request):
		overdue_jobs = [job for job in self.get_queryset() if job.is_overdue]
		serializer = JobListSerializer(overdue_jobs, many=True)
		return Response(serializer.data)
	
	@action(detail=False, methods=['get'])
	def by_status(self, request):
		status = request.query_params.get('status', None)
		if status:
			jobs = self.get_queryset().filter(status=status)
			serializer = JobListSerializer(jobs, many=True)
			return Response(serializer.data)
		return Response({"error": "Status parameter required"}, status=400)
	
class QuoteViewSet(viewsets.ModelViewSet):
	queryset = Quote.objects.select_related('customer').prefetch_related('line_items')
	filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
	search_fields = ['quote_number']
	filterset_fields = ['status', 'customer']
	ordering = ['-created_at']

	def get_serializer_class(self):
		if self.action == 'list':
			return QuoteListSerializer
		return QuoteDetailSerializer
	
class OperationViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Operation.objects.all()
	serializer_class = OperationSerializer
	filterset_fields =  ['job']
