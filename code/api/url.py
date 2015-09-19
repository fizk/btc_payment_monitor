from django.conf.urls import include, url
from django.contrib import admin
from api.views import *

urlpatterns = [
	# Login stuff
	url('^auth/', include('rest_framework.urls', namespace='rest_framework')),

	# View list of offers
	url('^monitor/$', bpm_payment_monitor_list.as_view()),

	# View particular offer
	url('monitor/(?P<obj_id>[0-9]+)/$', bpm_payment_monitor_detail.as_view()),

]

