from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from processor.models import *
from resultprocessor.models import *
from account.models import Student
import hashlib, datetime, random
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from random import *
import csv
import urllib2


@staff_member_required	
def transcript (request, action):
	if request.method == 'POST':
		student = request.POST.get('student', '')
		#school = request.POST.get('school', '')
		try:
			result = Result.objects.filter(user = student)
		except Result.DoesNotExist:
			pass
	return render_to_response('portal/transcript.html', {'student':Student.objects.all()}, context_instance=RequestContext(request))
	
	
@staff_member_required	
def publish_result (request):
	if request.method == 'POST':
		session = request.POST.get('session', '')
		school = request.POST.get('school', '')
		if school == 'SECONDARY':
			try:
				resultsummary = ResultSummary.objects.filter(session = session)
				for z in resultsummary:
					z.publish = True
					z.save()
				return render_to_response('dashboard/administrator/publish_result.html', {'message':'successful'}, context_instance=RequestContext(request))
			except ResultSummary.DoesNotExist:
				return render_to_response('dashboard/administrator/publish_result.html', {'error':'error'}, context_instance=RequestContext(request))
	return render_to_response('dashboard/administrator/publish_result.html', context_instance=RequestContext(request))

	
@staff_member_required	
def admin_card(request):
	num = request.POST.get('number', '')
	
	num = int(num)
	count = 1

	while count <= num:
		a = randint(520, 981)
		b = randint(520, 887)
		c = randint(117, 952)
		
		p = int(str(a*b) + str(c) + str(b) + str(a))
		try:
			Card.objects.get(pin = p)
			pass
		except Card.DoesNotExist:
		
			card = Card()
			card.pin = p
			card.save()
			count = count + 1
			
	return HttpResponseRedirect('/admin/processor/card/')

@staff_member_required	
def view_card(request):
	card = Card.objects.all()
	return render_to_response ('portal/view_card.html', {'card':card}, context_instance=RequestContext(request))

	
	
@staff_member_required	
def send_sms(request, action):
	if action == 'view':
		messages = Message.objects.all()
		render_to_response ('dashboard/administrator/sent_sms.html', {'message':message}, context_instance=RequestContext(request))
	else:
		if request.method == 'POST':
			sender = request.POST.get('sender_id', '')
			session = request.POST.get('session', '')
			school = request.POST.get('school', '')
			message = request.POST.get('message', '')
			
			try:			
				a = []
				for i in student_numbers:
					a.append(i.guardian_phone_number)
				numbers = ",".join(a)
				
				z = "http://www.hinzsms.com/components/com_spc/smsapi.php?username=myobss&password=12345&sender="+sender+"&recipient="+numbers+"&message="+text+"&"
				
				response = urllib2.urlopen(z)
				output = response.read()
				r = HttpResponse(output)
				for f in r:
					if 'OK' in f:
						z = 'SENT'
					else:
						z = 'NOTSENT'
				new = Message(sender_id = sender, phone_numbers = numbers, message_body = message)
				new.status = z
				new.save()
				
				return render_to_response ('dashboard/administrator/sms.html', {'message':'SMS was sent successfully'}, context_instance=RequestContext(request))
			except:
				pass
		else:
			return render_to_response ('dashboard/administrator/sms.html', context_instance=RequestContext(request))
	
	
	
@staff_member_required	
def card_csv(request):
	
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=cardpin.csv'

	p = Card.objects.filter(num_used = 0)
	
	writer = csv.writer(response)
	writer.writerow(['Unused Card Pin'])
	for i in p:
		#i = str(i)
		writer.writerow([i])
	
	return response
