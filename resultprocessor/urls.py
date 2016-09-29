from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
	
	url(r'^validation/$', 'resultprocessor.views.result_check', name='result_check'),
	#url(r'^display/$', 'resultprocessor.views.card_validate', name='result_view'),
	
	)