from django.conf.urls import patterns, include, url
from django.conf import settings
#from django.views.generic import RedirectView


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'views.home', name='homepage'),
	url(r'^portal/$', 'views.portal', name='portal'),
	url(r'^contact/$', 'views.contact', name='contact'),
	
	url(r'result/', include('resultprocessor.urls', namespace = 'result')),
	url(r'resultsheet/', include('resultsheet.urls', namespace = 'resultsheet')),
	url(r'^processor/', include('processor.urls', namespace = 'processor')),
	url(r'^blog/', include('blog.urls', namespace = 'blog')),
	url(r'^account/', include('account.urls', namespace = 'account')),
	
	
	# accounts related

	# login / logout urls
	url(r'^login/$', 'account.views.login', name='login'),
	url(r'^logout/$', 'account.views.logout', name='logout'),
	
	# change password urls
	url(r'^password-change/$', 'django.contrib.auth.views.password_change', name='password_change'),
	url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),

	# restore password urls
	url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
	url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
	url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
	url(r'^password-reset/complete/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

	#admin related
	
	url(r'^admin/processor/card/add/generate', 'processor.views.admin_card'),
	url(r'^admin/processor/card/print/', 'processor.views.card_csv'),
	url(r'media/(?P<path>.*)', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
	

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^grappelli/', include('grappelli.urls')),
	url(r'^admin/', include(admin.site.urls)),
)