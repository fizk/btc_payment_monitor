from django.shortcuts import render
from monitor.models import BPMPaymentMonitor
from api.serializers import BPMPaymentMonitorSerializer
from django.http import HttpResponseForbidden, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ParseError
from rest_framework import status, permissions, serializers
from pprint import pprint

# 

class bpm_payment_monitor_list(APIView):
	"""
	List offers, or create a new offer.
	"""


# FIXME:
#	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, format=None):
		# Check if user has access (i.e., is logged in).
#		self.check_object_permissions(self.request, request.data)

#		bpm_monitor_objs = Offer.objects.filter(pk=request.id)
		bpm_monitor_objs = BPMPaymentMonitor.objects.all()

		# Serialize everything
		serializer = BPMPaymentMonitorSerializer(bpm_monitor_objs, many=True)

		return Response(serializer.data)


class bpm_payment_monitor_detail(APIView):
	"""
	Retrieve and edit an offer. They cannot be deleted.
	"""

	# FIXME: Comment

#	permission_classes = (BBIsOwnerRW,)

	def get_object(self, pk):
		try:
			obj = BPMPaymentMonitor.objects.get(pk=pk)

		except BPMPaymentMonitor.DoesNotExist:
			raise Http404

#		self.check_object_permissions(self.request, obj)

		return obj

	def get(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = BPMPaymentMonitorSerializer(snippet)

		return Response(serializer.data)

