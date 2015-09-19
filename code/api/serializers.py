from django.forms import widgets
from rest_framework import serializers
from monitor.models import BPMPaymentMonitor
from pprint import pprint

class BPMPaymentMonitorSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	created_at = serializers.DateTimeField(read_only=True, format='iso-8601')
	address = serializers.CharField(read_only=False)
	confirmations_required = serializers.IntegerField(read_only=False) 
	cancelled = serializers.BooleanField(read_only=False)
	block_number_start = serializers.IntegerField(read_only=False)             
	block_number_scanned = serializers.IntegerField(read_only=True)
	amount_desired = serializers.IntegerField(read_only=False)                     
	amount_paid = serializers.IntegerField(read_only=True)         
	goal_reached = serializers.BooleanField(read_only=True)           
	goal_reached_at = serializers.DateTimeField(read_only=True) 
	
	def create(self, validated_data):
		"""
		Create and return a new `BPMPaymentMonitor` instance, given the validated data.
		"""

		return BPMPaymentMonitor.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing `BPMPaymentMonitor` instance, given the validated data.
		"""
       
		instance.save()

		return instance

