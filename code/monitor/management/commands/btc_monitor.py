from django.core.management.base import BaseCommand, CommandError
from monitor.models import *

import bitcoin
import bitcoin.rpc
from bitcoin.core import CBlock, b2lx, b2x, x, lx

import struct
import sys
import time
import datetime
import random


# FIXME: How many blocks to loop through?
# FIXME: Limitation, an address can only be monitored once ...
# FIXME: TimeZone problem

class Command(BaseCommand):
	help = 'Monitors payments on the Bitcoin network'

	debug_level = 1 

	# Write out some text message
	def say(self, txt):
		return self.stdout.write("[%s] btc_payment_monitor/btc_monitor: %s" % (time.ctime(), txt) )

	#
	# Write out a debug message 
	# (if debug level is appropriate)
	#

	def debug(self, txt_debug_level, txt):
		if self.debug_level >= txt_debug_level:
			return self.say(txt)

		else:
			return False
    
	def add_arguments(self, parser):
		parser.add_argument('debug_level', nargs='+', type=int)

	# 
	# Update the monitoring data we use
	# to watch for new payments
	#

	def update_monitoring_data(self):
		self.debug(4, 'Updating monitoring data ... ')
	
		#
		# Clean out addresses we used before,
		# and clean out the dict-object we
		# used to map between addresses and DB-objects
		#

		self.monitor_addresses = []
		self.monitor_addresses_obj_mapping = {}

		#
		# Find all the BPMPaymentMonitor objects
		# that we should watch during the next run
		# 

		self.bpm_monitor_objs = BPMPaymentMonitor.objects.filter(
			goal_reached=False
		).filter(
			amount_desired__gte=0
		).filter(
			cancelled=False
		)


		# 
		# Figure out from what block we should start;
		# generally, we want to be 'inclusive', so that
		# we might scan the same block more than once.
		# Here, we set the start at the lowest block
		# number specified among the items we should watch
		# -- the specification being either the last block
		# number scanned, or the block number we were instructed
		# to begin at
		#

		for bpm_monitor_objs_cnt in range(0, len(self.bpm_monitor_objs)):
			self.monitor_addresses.append(self.bpm_monitor_objs[bpm_monitor_objs_cnt].address.address)
			self.monitor_addresses_obj_mapping[self.bpm_monitor_objs[bpm_monitor_objs_cnt].address.address] = bpm_monitor_objs_cnt

			if (self.bpm_monitor_objs[bpm_monitor_objs_cnt].block_number_scanned == 0):
				self.bpm_monitor_objs[bpm_monitor_objs_cnt].block_number_scanned = self.bpm_monitor_objs[bpm_monitor_objs_cnt].block_number_start

			if (self.bpm_monitor_objs[bpm_monitor_objs_cnt].block_number_start < self.block_number_current):
				self.block_number_current = self.bpm_monitor_objs[bpm_monitor_objs_cnt].block_number_scanned

		self.debug(1, 'Figured what next block would be scanned; block_number=%i' % self.block_number_current)

		self.debug(4, '... done')

		return True

	#
	# Update number of confirmations associated
	# with each active record still active in 
	# BPMPaymentMonitor. Here, we will ask bitcoind 
	# for number of confirmations for each record.

	def update_confirmations(self):
		self.debug(2, 'Updating confirmations ...')

		#
		# Get all active monitors
		#

		for bpm_monitor_objs_cnt in range(0, len(self.bpm_monitor_objs)):
			pm_obj = self.bpm_monitor_objs[bpm_monitor_objs_cnt]
			pm_obj_transactions = pm_obj.transactions.all()

			#
			# Now, for each transaction associated with that, 
			# get the raw transaction, get the number of confirmations
			# and save that with the transaction.
			#

			for bpm_transaction in pm_obj_transactions:
				block_vtx_info = self.proxy._call('getrawtransaction', bpm_transaction.transaction_hash, 1)

				#
				# This should never happen
				#

				if ((block_vtx_info['vout'][bpm_transaction.vout]['value'] * 100000000) != bpm_transaction.amount):
					self.say("WARNING: Transaction fetched from bitcoind, with the same hash and vout as saved earlier in DB did not have same amount!")

				else:
					self.debug(4, 'Updated transaction with newer confirmation count; pk=%i, tx=%s, vout=%i, confirmations=%i' % (bpm_transaction.pk, bpm_transaction.transaction_hash, bpm_transaction.vout, bpm_transaction.confirmations))
					bpm_transaction.confirmations = block_vtx_info['confirmations'] 
					bpm_transaction.save()
	

		self.debug(2, '... done')

	def handle(self, *args, **options):
		self.say('Initializing ...')

		# 
		# Set debug level
		#

		try:
			self.debug_level = options['debug_level'][0]

		except:
			self.debug_level = 1

		self.debug(1, "Set debug level; debug_level=%i" % self.debug_level)
		
		#
		# Connect to the bitcoind server
		#

		bitcoin.SelectParams('testnet')
		self.proxy = bitcoin.rpc.Proxy()

		#
		# Get the latest block number
		#

		bitcoin_getinfo = self.proxy._call('getinfo')
		self.block_number_current = bitcoin_getinfo['blocks'] - 1

		#
		# Update monitoring data
		# 

		self.update_monitoring_data()

		self.say('... initialized. Started processing.')

		while 1:

			# Try to get next block
			try:
				block = self.proxy.getblock(self.proxy.getblockhash(self.block_number_current))

			# If that fails, sleep -- we 
			# probably just hit the end of
			# the currently aggreed on blocks
			except IndexError:
				self.debug(1, "No newer block found... ")

				self.update_confirmations()

				self.debug(1, 'Now sleeping')

				time.sleep(32)

				self.update_monitoring_data()


				continue

			self.debug(1, "Processing block; no=%s, hash=%s" % (str(self.block_number_current), b2lx(block.GetHash())))

			# Get transaction count within block
			block_vtx_len = len(block.vtx)

			#
			# For each transaction within a block ...
			# 

			for block_vtx_cnt in range(0, block_vtx_len):
				#
				# Fetch the transaction-object from bitcoind
				#
				block_vtx = block.vtx[block_vtx_cnt]
				self.debug(2, "Processing transaction; tx=%s" % b2lx(block_vtx.GetHash()))

				block_vtx_info = self.proxy._call('getrawtransaction', b2lx(block_vtx.GetHash()), 1)

				# Get number of vouts in this transaction
				block_vtx_vout_len = len(block_vtx_info['vout'])

				#
				# For each vout in the current transaction
				#

				for block_vtx_vout_cnt in range(0, block_vtx_vout_len):	
					# Check if the transaction has any addresses
					try:
						block_vtx_info['vout'][block_vtx_vout_cnt]['scriptPubKey']['addresses'].__str__()

					# If not, skip it
					except:
						continue	

					self.debug(3, "Transaction payout addresses=%s" % block_vtx_info['vout'][block_vtx_vout_cnt]['scriptPubKey']['addresses'])


					# Now, for each address in our monitoring array,
					# we check if each an every one matches any of those
					# in the current transaction.
					#
					# If that is the case, collect some data so that
					# we can do calculations with it pertaining to our monitoring
					# (only if not done before!)

					for self.monitor_addresses_cnt in range(0, len(self.monitor_addresses)):
						monitor_address_found = True

						#
						# Check if any address is found ...
						#

						try:
							block_vtx_info['vout'][block_vtx_vout_cnt]['scriptPubKey']['addresses'].index(self.monitor_addresses[self.monitor_addresses_cnt])
						
						except ValueError:
							monitor_address_found = False

						if (monitor_address_found == True):
							self.debug(2, "Found payment to address being monitored; tx=%s, address=%s" % (b2lx(block_vtx.GetHash()), self.monitor_addresses[self.monitor_addresses_cnt]))


							# NOTE:
							# It is possible to have multiple addresses picking up the same payment --
							# but we do not allow that. If we would, we might risk that we believe payment has
							# been received in the address specified in the watch (which is correct), but 
							# then the other address specified in the transaction picks up the money and leaves, 
							# leaving nothing with us. Hence, they might use our service without paying.
							#
							
							if (len(block_vtx_info['vout'][block_vtx_vout_cnt]['scriptPubKey']['addresses']) > 1 ):
								self.say("Found payment, but it has multiple destinations; cannot trust that the destination address specified in our watch request is the only recipient -- will not consider this as a payment as a result. Skipping. Transaction; tx=%s" % b2lx(block_vtx.GetHash()))
								continue 

							# Now, we know that one of the addresses
							# we are monitoring received a payment.
							# Check if we have any information about this
							# from a previous run. If so, do nothing about this.

							# Find the monitoring-objects via the linkage dict
							pm_obj = self.bpm_monitor_objs[self.monitor_addresses_obj_mapping[self.monitor_addresses[self.monitor_addresses_cnt]]]

							# Calculate the value of the vout
							trans_value = int(block_vtx_info['vout'][block_vtx_vout_cnt]['value'] * 100000000)

							#						
							# Try to find this particular vout, transaction and value
							# among previous transactions that belong to this monitoring object
							#

							trans_arr = pm_obj.transactions.filter(
								transaction_hash = b2lx(block_vtx.GetHash())
							).filter(
								amount = trans_value
							).filter(
								vout = block_vtx_vout_cnt
							)

							#
							# If we do not have this transaction on record
							# (among the ones associated with the current monitoring object),
							# put it on the record.
							#

							if len(trans_arr) == 0:
								self.debug(2, "Payment not already registered by us -- did create transaction in DB")
								transaction = BPMTransactions()
								transaction.transaction_hash = b2lx(block_vtx.GetHash())
								transaction.amount = trans_value
								transaction.vout = block_vtx_vout_cnt
								transaction.confirmations = block_vtx_info['confirmations']
								transaction.save()

								pm_obj.transactions.add(transaction)
								pm_obj.save()

								#
								# Do updating on the monitoring object
								#

								self.debug(3, "Updating amoint received, etc. ..")	
								pm_obj.update_calculations()
								self.debug(3, "... finished")

							else:
								self.debug(2, "Payment already registered by us -- did NOT create transaction in DB")


			# For each we are monitoring, save
			# what block we have reached

			for pm_obj in self.bpm_monitor_objs:
				pm_obj.block_number_scanned = self.block_number_current

				# Only save occationally to save resources
				# -- not much will be lost anyway, and over 
				# time we might save quite a lot of resources

				if (random.randrange(0, 10) == 5):
					pm_obj.save()

			# Increment block number for next round 
			self.block_number_current += 1
