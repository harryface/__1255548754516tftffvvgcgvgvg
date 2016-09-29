from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from processor.models import Card
from django.template import RequestContext
from resultprocessor.models import *
from resultsheet.models import *
from django.contrib import auth
from django.core.urlresolvers import reverse

	
#secondary school only	
def result_check(request):
	if request.method == 'POST':
		admission_num = request.POST.get('admission_num', '')
		token = request.POST.get('token', '')
		term = request.POST.get('term', '')
		subclass = request.POST.get('subclass', '')
		arm = request.POST.get('arm', '')
		session = request.POST.get('session', '')
		
		try:
			card = Card.objects.get(pin = token)
			if subclass == 'JSS1' or subclass == 'JSS2' or subclass == 'JSS3' or subclass == 'SSS1' or subclass == 'SSS2' or subclass == 'SSS3':
				try:
					student = StudentProfile.objects.get(admission_num = admission_num)
				except StudentProfile.DoesNotExist:
					return render_to_response ('result/check_result.html', {'error':'Student does not exist'})
				try:
					result_sum = ResultSummary.objects.get(student = student, level = subclass, class_arm = arm, term = term, session = session, publish = True)
				except ResultSummary.DoesNotExist:
					return render_to_response ('result/check_result.html', {'error':'Result not ready yet'})
				
				classnum = ResultSummary.objects.filter(level = subclass, class_arm = arm, term = term, session = session)
				countnum = []
				for i in classnum:
					countnum.append(i.average)
				numnum = len(countnum)
				
				if card.user == student and card.level == subclass and card.session == session and card.term == term and card.num_used <= 6:
					card.num_used = card.num_used + 1
					card.save()
					result_summary = ResultSummary.objects.filter(student = student, level = subclass, class_arm = arm, term = term, session = session)
					result = Result.objects.filter(student = student, level = subclass, class_arm = arm, term = term, session = session)
					if term == "THIRD":
						annual_summary = AnnualSummary.objects.filter(student = student, level = subclass, class_arm = arm, session = session)
						annual = Annual.objects.filter(student = student, level = subclass, class_arm = arm, session = session)
						return render_to_response('result/annual_result.html', {'result' : result, 'student': user, 'summary' : result_summary, 'numnum':numnum, 'annual' : annual, 'annualsummary' : annual_summary}, context_instance=RequestContext(request))
					else:
						return render_to_response('result/result_update.html', {'result' : result, 'student': student, 'summary' : result_summary, 'numnum':numnum}, context_instance=RequestContext(request))
				
				elif card.user is None:
						card.user = student
						card.level = subclass
						card.session = session
						card.term = term
						card.num_used = card.num_used + 1
						card.save()
						
						result = Result.objects.filter(student = student, level = subclass, class_arm = arm, term = term, session = session)
						if term == "THIRD":
							annual_summary = AnnualSummary.objects.filter(student = student, level = subclass, class_arm = arm, session = session)
							annual = Annual.objects.filter(student = student, level = subclass, class_arm = arm, session = session)
							return render_to_response('result/annual_result.html', {'result' : result, 'student': student, 'summary' : result_summary, 'numnum':numnum, 'annual' : annual, 'annualsummary' : annual_summary}, context_instance=RequestContext(request))
						else:
							return render_to_response('result/result_update.html', {'result' : result, 'student': student, 'summary' : result_summary, 'numnum':numnum}, context_instance=RequestContext(request))
				else:
					return render_to_response('result/check_result.html', {'error':'You have exhausted your card allowance'}, context_instance=RequestContext(request))
								
		except Card.DoesNotExist:
			return render_to_response ('result/check_result.html', {'error':'card does not exist'})
	return render_to_response('result/check_result.html', context_instance=RequestContext(request))

