from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

	url(r'^/$', 'blog.views.load_post', name = 'load_post'),
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'blog.views.post_detail', name='post_detail'),
	url(r'^edit/post/(?P<id>\d+)/$', 'blog.views.edit_post', name = 'edit_post'),
	url(r'^publish/(?P<page>.*)/$', 'blog.views.publish_post', name = 'publish_post'),
	url(r'^edit/gallery/(?P<id>\d+)/$', 'blog.views.edit_gallery', name = 'edit_gallery'),
	
	#search
	url(r'^search/$', 'blog.views.search', name='search'),
	
	)