from django.shortcuts import render
from monitor.models import BPMPaymentMonitor, BPMAddress
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
	List payment addresses being monitors, or create a new one.
	"""

# FIXME:
#	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, format=None):
		# Check if user has access (i.e., is logged in).
#		self.check_object_permissions(self.request, request.data)


		try:
			ids_str = request.GET.get('id')
			ids = ids_str.split(',')

		except:
			raise ParseError('Could not parse id numbers')


		try:
			for i in range(0, len(ids)):
				ids[i] = int(ids[i])

		except:
			raise ParseError('Could not convert id numbers to integers.')

		bpm_monitor_objs = BPMPaymentMonitor.objects.filter(pk__in=ids)

		# Serialize everything
		serializer = BPMPaymentMonitorSerializer(bpm_monitor_objs, many=True)

		for i in range(0, len(serializer.data)):
			serializer.data[i]['address'] = bpm_monitor_objs[i].address.address

		return Response(serializer.data)

	def post(self, request, format=None):
		# Check if user has access
		self.check_object_permissions(self.request, request.data)
                
		# Serialize everything
		serializer = BPMPaymentMonitorSerializer(data=request.data)

		if (serializer.is_valid()):

			# FIXME: Try re-using older object...
			bpm_address = BPMAddress.objects.filter(address=serializer.initial_data['address'])

			if (len(bpm_address) == 0):
				bpm_address = BPMAddress()
				bpm_address.address = serializer.initial_data['address']
				bpm_address.save()

			else:
				bpm_address = bpm_address[0]

			serializer.save(
				address = bpm_address
			)

			return Response(serializer.data, status=status.HTTP_201_CREATED)
                
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class bpm_payment_monitor_detail(APIView):
	"""
	Retrieve and edit a monitoring. They cannot be deleted.
	"""

	# FIXME: Comment

#	permission_classes = (BBIsOwnerRW,)

	def get_object(self, obj_id):
		try:
			obj = BPMPaymentMonitor.objects.get(pk=obj_id)

		except BPMPaymentMonitor.DoesNotExist:
			raise Http404

#		self.check_object_permissions(self.request, obj)

		return obj

	def get(self, request, obj_id, format=None):
		obj = self.get_object(obj_id)

		serializer = BPMPaymentMonitorSerializer(obj, many=False)

		serializer.data.serializer._data['address'] = obj.address.address 

		return Response(serializer.data)

	def put(self, request, obj_id, format=None):
		obj = self.get_object(obj_id)

		serializer = BPMPaymentMonitorSerializer(obj, many=False)

		return Response(serializer.data)

