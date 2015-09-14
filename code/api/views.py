from django.shortcuts import render
from monitor.models import BPMPaymentMonitor, BPMAddress
from api.serializers import BPMPaymentMonitorSerializer
from django.http import HttpResponseForbidden, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ParseError
from rest_framework import status, permissions, serializers
from pycoin.key.validate import is_address_valid as pycoin_address_validate
from pprint import pprint
from btc_payment_monitor.settings import BPM_NET

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

		#	
		# Try to get 'id' parameter used in request;
		# this allows our users to pass on a number
		# of arguments in one request
		#

		try:
			ids_str = request.GET.get('id')
			ids = ids_str.split(',')

		except:
			raise ParseError('Could not parse id numbers')


		#
		# And now, for all 'ID's from request, convert
		# to integer-type -- serves as an input check also,
		# as 'int()' only accepts strings that can be
		# converted to integers.
		#

		try:
			for i in range(0, len(ids)):
				ids[i] = int(ids[i])

		except:
			raise ParseError('Could not convert id numbers to integers.')


		#
		# Get list of monitoring objects that match the request parameter
		#

		bpm_monitor_objs = BPMPaymentMonitor.objects.filter(pk__in=ids)

		# Serialize everything
		serializer = BPMPaymentMonitorSerializer(bpm_monitor_objs, many=True)

		#
		# Sanity check: Make sure every item in the DB-objects array matches
		# those in the serialized objects-array
		#

		for i in range(0, len(serializer.data)):
			if (serializer.data[i]['id'] != bpm_monitor_objs[i].pk):
				raise ParseError('Serialized objects do not match those fed into serializer')

			# Put in the address (as string) in the serialized objects, replacing the object
			serializer.data[i]['address'] = bpm_monitor_objs[i].address.address

		# Return the serialized data
		return Response(serializer.data)

	def post(self, request, format=None):
		# Check if user has access
		self.check_object_permissions(self.request, request.data)
                
		# Serialize everything
		serializer = BPMPaymentMonitorSerializer(data=request.data)

		#
		# No need to provide us with the 'cancelled' field;
		# we will define it if undefined
		#

		if (serializer.initial_data.has_key('cancelled') == False):
			serializer.initial_data['cancelled'] = False

		#
		# It is, however, not allowed to create a monitoring
		# that is cancelled straight from the start
		#

		if (serializer.initial_data['cancelled'] == True):
			raise ParseError('Creating already cancelled monitoring is not allowed') 

		if (serializer.is_valid()):
			# Check if address provided is valid.
			address_type = pycoin_address_validate(serializer.initial_data['address'])

			#
			# Check if address-type matches the network we run on
			# - and if it is valid.
			#

			if ((address_type == 'BTC') and (BPM_NET == 'mainnet')):
				address_type_ok = True

			elif ((address_type == 'XTN') and (BPM_NET == 'testnet3')):
				address_type_ok = True

			else:
				# User provided invalid address
				raise ParseError('Key address is invalid: syntax error, or does not match the network we run on (which is: ' + BPM_NET + ')')
			
			# Check if we can find provided address in 
			# our registry of addresses	
			bpm_address = BPMAddress.objects.filter(address=serializer.initial_data['address'])

			# Nothing found, create a new record	
			if (len(bpm_address) == 0):
				bpm_address = BPMAddress()
				bpm_address.address = serializer.initial_data['address']
				bpm_address.save()

			# Found, use previous record
			else:
				bpm_address = bpm_address[0]

			# Save monitoring 
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

# FIXME: Permissions
#	permission_classes = (BBIsOwnerRW,)

	def get_object(self, obj_id):
		try:
			obj = BPMPaymentMonitor.objects.get(pk=obj_id)

		except BPMPaymentMonitor.DoesNotExist:
			raise Http404

# FIXME: Permissions
#		self.check_object_permissions(self.request, obj)

		return obj

	def get(self, request, obj_id, format=None):
		# Try to fetch the requested monitoring from DB
		obj = self.get_object(obj_id)

		# Serialize what was fetched
		serializer = BPMPaymentMonitorSerializer(obj, many=False)

		# Put address (as string) in place of an address-object
		serializer.data.serializer._data['address'] = obj.address.address 

		# Serialize data
		return Response(serializer.data)

	def put(self, request, obj_id, format=None):
		obj = self.get_object(obj_id)

		serializer = BPMPaymentMonitorSerializer(obj, data=request.data, many=False, partial=True)

		#
		# We only allow cancellation of monitoring; not alteration
		#

		if ( 
			(serializer.initial_data['cancelled'] != True) or
			(len(serializer.initial_data) >= 2)
		):
			raise serializers.ValidationError("Only the cancelled field is allowed in PUT requests, and it can only be True.")


		if (serializer.is_valid()):
			# FIXME: Do this properly, "right"
			obj.cancelled = serializer.initial_data['cancelled']
			obj.save()

			serializer.save(
			)

			return Response(serializer.data)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
