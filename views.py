from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


def portal(request):
	return render_to_response('home/portal.html', context_instance=RequestContext(request))
	
def home(request):
	return render_to_response('home/index.html', context_instance=RequestContext(request))
	
def contact(request):
	return render_to_response('contact.html', context_instance=RequestContext(request))
	
	
def csrf_failure(request, reason=""):
	ctx = {'message': 'please kindly reload your browser'}
	return render_to_response('500.html', ctx)
	
	