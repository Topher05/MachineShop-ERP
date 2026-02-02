from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'contacts', views.ContactViewSet, basename='contact')
router.register(r'jobs', views.JobViewSet, basename='job')
router.register(r'quotes', views.QuoteViewSet, basename='quote')
router.register(r'operations', views.OperationViewSet, basename='operation')

urlpatterns = [
	path('', include(router.urls)),
]