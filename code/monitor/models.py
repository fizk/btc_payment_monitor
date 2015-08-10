from django.db import models
from datetime import datetime

# Create your models here.

class BPMAddress(models.Model):
	address = models.CharField(null=False, max_length=64)

class BPMAddress_from(models.Model):
	address = models.CharField(null=False, max_length=64)

class BPMTransactions(models.Model):
	transaction_hash = models.CharField(null=False, max_length=92)
	vout = models.PositiveIntegerField(null=False)
	amount = models.BigIntegerField(null=False)
	confirmations = models.BigIntegerField(null=False)

class BPMPaymentMonitor(models.Model):
	created_at = models.DateTimeField(null=False, auto_now_add=True)	 # When the monitoring was created
	address = models.ForeignKey(BPMAddress, null=False)			 # The address which we shall watch for payments
	confirmations_required = models.PositiveSmallIntegerField(null=False, default=16) # We want an extra layer of security, we like sleeping.
	cancelled = models.BooleanField(default=False)
	block_number_start = models.PositiveIntegerField(null=False)		 # At what block to start checking
	block_number_scanned = models.PositiveIntegerField(null=False, default=0)
       	amount_desired = models.BigIntegerField(null=False)			 # Amount, in satoshi units
	amount_paid = models.BigIntegerField(null=False, default=0)		 # Ditto.
	amount_reached = models.BooleanField(default=False)			 # Indicates that the address has received 'amount_desired'
        amount_reached_at = models.DateTimeField(null=True, auto_now_add=False) # Indicate when (approximately) the address reached amount_desired
	addresses_from = models.ManyToManyField(BPMAddress_from)		 
	transactions = models.ManyToManyField(BPMTransactions)

	def update_amount_paid(self):
		amount_paid_total = 0

		for transaction_item in self.transactions.all():
			amount_paid_total += transaction_item.nValue 
         
		self.amount_paid = amount_paid_total

		# FIXME: confirmations_required also
		if (self.amount_paid >= self.amount_desired) :
			self.amount_reached = True
			self.amount_reached_at = datetime.now()

		else:
			self.amount_reached = False

		self.save()