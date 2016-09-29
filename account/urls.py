from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# Examples:
	url(r'^administrator/$', 'account.views.admin_dashboard', name='admin_account'),
	url(r'^student/$', 'account.views.student_account', name='student_account'),
	url(r'^registration/$', 'account.views.new_student', name='registration'),

	url(r'^create/student/$', 'account.views.student_account', name = 'student_account'),
	url(r'^create/administrator/$', 'account.views.admin_account', name = 'administrator_account'),
	
	url(r'^edit/(?P<account>.*)/$', 'account.views.edit_account', name = 'edit_account'),
	url(r'^view/(?P<account>.*)/$', 'account.views.view_account', name = 'view_account'),
	url(r'^deactivate/(?P<id>.*)/$', 'account.views.deactivate_account', name = 'deactivate'),
	url(r'^profile/(?P<actionz>[-\w]+)/$', 'account.views.edit', name='edit_profile'),
)