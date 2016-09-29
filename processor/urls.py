from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
	url(r'^transcript/(?P<action>.*)/$', 'processor.views.transcript', name='transcript'),
	url(r'^sms/(?P<action>.*)/$', 'processor.views.send_sms', name='sms'),
	url(r'^card/$', 'processor.views.view_card', name='card'),
	url(r'^compute/result/$', 'processor.views.publish_result', name='compute_result'),
	
	)