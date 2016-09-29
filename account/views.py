from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from account.models import *


def login (request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	if request.method == 'POST':
		user = auth.authenticate(username = username, password = password)
		if user is not None:
			try:
				if StudentProfile.objects.get(user = user) or PrimaryProfile.objects.get(user = user) or KindergatenProfile.objects.get(user = user) or PreKindergatenProfile.objects.get(user = user):
					auth.login(request, user)
					return HttpResponseRedirect('/account/student/')
				else:
					profile = StudentProfile.objects.get(user = user)
			except StudentProfile.DoesNotExist:
				pass
			try:
				if user.is_staff:
					auth.login(request, user)
					return HttpResponseRedirect('/account/administrator/')
			except:
				pass
		else:
			return HttpResponseRedirect('/account/invalid/')


@login_required
def logout (request):
	auth.logout(request)
	return HttpResponseRedirect('/')

	
@login_required
def edit (request, actionz = None):
	user = request.user
	try:
		profile = StudentProfile.objects.get(user = user)
		if actionz == "edit":
			return render_to_response('dashboard/student/edit_profile.html', {'user' : user, 'profile':profile, 'edit':'edit'}, context_instance=RequestContext(request))
		elif actionz == "view":
			return render_to_response('dashboard/student/edit_profile.html', {'user' : user, 'profile':profile}, context_instance=RequestContext(request))
	except StudentProfile.DoesNotExist:
		pass
	return HttpResponseRedirect('/')
		
	
@staff_member_required
@login_required	
def admin_dashboard(request):
	user = request.user
	check = AdminProfile.objects.get(user = user)
	return render_to_response('dashboard/administrator/index.html', {'user':user, 'profile':check})
	
@login_required	
def student_dashboard(request):
	user = request.user
	try:
		check =StudentProfile.objects.get(user = user)
		return render_to_response('dashboard/student/index.html', {'user':user, 'profile':check})
	except StudentProfile.DoesNotExist:
		pass
	try:
		check = PrimaryProfile.objects.get(user = user)
		return render_to_response('dashboard/student/index.html', {'user':user, 'profile':check})
	except PrimaryProfile.DoesNotExist:
		pass
	try:
		check = KindergatenProfile.objects.get(user = user)
		return render_to_response('dashboard/student/index.html', {'user':user, 'profile':check})
	except KindergatenProfile.DoesNotExist:
		pass
	try:
		check = PreKindergatenProfile.objects.get(user = user)
		return render_to_response('dashboard/student/index.html', {'user':user, 'profile':check})
	except PreKindergatenProfile.DoesNotExist:
		pass
	
	
@login_required
@staff_member_required
def student_account (request):
	c = {}
	c.update(csrf(request))
		
	if request.method == 'POST':
		surname = request.POST.get('surname', '')
		first_name = request.POST.get('first_name', '')
		middle_name = request.POST.get('middle_name', '')
		address = request.POST.get('address', '')
		admission_num = request.POST.get('admission_num', '')
		state = request.POST.get('state', '')
		guardian_name = request.POST.get('guardian_name', '')
		country = request.POST.get('country', '')
		sex = request.POST.get('gender', '')
		school = request.POST.get('school', '')
		phone = request.POST.get('guardian_phone_number', '')
		"""if 'headshot' in request.FILES:
			headshot = request.FILES['headshot']
		else :
			headshot = None"""
		headshot = request.FILES.get('headshot', '')	
		if admission_num and surname and first_name and school:
			try:
				user = User.objects.get(username = admission_num)
				#print error this admission number has been registered
			except User.DoesNotExist:
				user = User.objects.create(username = admission_num, password = surname, first_name = first_name, last_name = middle_name)
				
				if school == 'secondary':
					student = StudentProfile.objects.create(surname = surname, address = address, first_name = first_name, admission_num = admission_num, state = state, guardian_name = guardian_name, country = country, middle_name = middle_name, sex = sex, headshot = headshot, guardian_phone_number = phone, user = user)
				elif school == 'primary':
					student = PrimaryProfile.objects.create(surname = surname, address = address, middle_name = middle_name, first_name = first_name,admission_num = admission_num, state = state, guardian_name = guardian_name, country = country, sex = sex, headshot = headshot, guardian_phone_number = phone, user = user)
				elif school == 'kindergarten':
					student = KindergatenProfile.objects.create(surname = surname, middle_name = middle_name, address = address, first_name = first_name,admission_num = admission_num, state = state, guardian_name = guardian_name, country = country, sex = sex, headshot = headshot, guardian_phone_number = phone, user = user)
				else:
					student = PreKindergatenProfile.objects.create(surname = surname, middle_name = middle_name, address = address, first_name = first_name,admission_num = admission_num, state = state, guardian_name = guardian_name, country = country, sex = sex, headshot = headshot, guardian_phone_number = phone, user = user)
				return render_to_response('dashboard/administrator/create_student.html', {'message': 'success'}, context_instance=RequestContext(request))
		else:
			pass
			return render_to_response('dashboard/administrator/create_student.html', {'error': 'failure'}, context_instance=RequestContext(request))
	return render_to_response('dashboard/administrator/create_student.html', context_instance=RequestContext(request))
	
	
@login_required
@staff_member_required	
def admin_account (request):
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':
		surname = request.POST.get('surname', '')
		first_name = request.POST.get('first_name', '')
		middle_name = request.POST.get('middle_name', '')
		address = request.POST.get('address', '')
		state = request.POST.get('state', '')
		lga = request.POST.get('lga', '')
		country = request.POST.get('country', '')
		gender = request.POST.get('gender', '')
		phone = request.POST.get('phone', '')
		if 'headshot' in request.FILES:
			headshot = request.FILES['headshot']
		else :
			headshot = None
	
		if phone and surname and first_name:
			try:
				User.objects.get(username = phone)
				#print error this admission number has been registered
			except User.DoesNotExist:
				user = User.objects.create(username = phone, password = surname, first_name = first_name, last_name = middle_name)
				user.is_staff = True
				user.is_superuser = True
				user.save()
				admin = AdminProfile.objects.create(surname = surname, address = address, mobile_phone = phone, country = country, sex = gender, headshot = headshot, user = user, first_name = first_name, middle_name = middle_name, state = state)
				#admin.save()
				return render_to_response('dashboard/administrator/create_admin.html', {'message': 'success'}, context_instance=RequestContext(request))
		else:
			pass
			return render_to_response('dashboard/administrator/create_admin.html', {'error': 'failure'}, context_instance=RequestContext(request))
	return render_to_response('dashboard/administrator/create_admin.html', context_instance=RequestContext(request))

	
@login_required
@staff_member_required	
def view_account (request, account):
	if account == 'admin':
		accounts = AdminProfile.objects.all()
		name = []
		for b in accounts:
			a = b.user.first_name + ' ' + b.user.last_name
			name.append(a)
	elif account == 'students':
		accounts = StudentProfile.objects.all()
		name = []
		for b in accounts:
			a = b.user.first_name + ' ' + b.user.last_name
			name.append(a)
	return render_to_response('account_view.html', {'account':accounts, 'name':name}, context_instance=RequestContext(request))
	

@login_required
@staff_member_required	
def edit_account (request, account):
	if account == 'admin':
		accounts = AdminProfile.objects.all()
		name = []
		for b in accounts:
			a = b.user.first_name + ' ' + b.user.last_name
			name.append(a)
	elif account == 'students':
		accounts = StudentProfile.objects.all()
		name = []
		for b in accounts:
			a = b.user.first_name + ' ' + b.user.last_name
			name.append(a)
	
	return render_to_response('account_view.html', {'account':accounts, 'name':name}, context_instance=RequestContext(request))
	
@staff_member_required	
@login_required
def deactivate_account(request, id):
	try:
		check =StudentProfile.objects.get(id = id)
		check.delete()
		return HttpResponseRedirect('/')
	except StudentProfile.DoesNotExist:
		pass
	try:
		check = PrimaryProfile.objects.get(id = id)
		check.delete()
		return HttpResponseRedirect('/')
	except PrimaryProfile.DoesNotExist:
		pass
	try:
		check = KindergatenProfile.objects.get(id = id)
		check.delete()
		return HttpResponseRedirect('/')
	except KindergatenProfile.DoesNotExist:
		pass
	try:
		check = PreKindergatenProfile.objects.get(id = id)
		check.delete()
		return HttpResponseRedirect('/')
	except PreKindergatenProfile.DoesNotExist:
		pass
	try:
		check = AdminProfile.objects.get(id = id)
		check.delete()
		return HttpResponseRedirect('/')
	except AdminProfile.DoesNotExist:
		pass
		
	return render_to_response('dashboard/deactivate_account.html', context_instance=RequestContext(request))
	
	
def new_student (request):
	if request.method == 'POST':
		surname = request.POST.get('surname', '')
		first_name = request.POST.get('first_name', '')
		middle_name = request.POST.get('middle_name', '')
		address = request.POST.get('address', '')
		state = request.POST.get('state', '')
		guardian_name = request.POST.get('guardian_name', '')
		country = request.POST.get('country', '')
		sex = request.POST.get('gender', '')
		school = request.POST.get('school', '')
		phone = request.POST.get('guardian_phone_number', '')
		if 'headshot' in request.FILES:
			headshot = request.FILES['headshot']
		else :
			headshot = None
			
		if phone and surname and first_name and school:
			try:
				username = phone + first_name
				user = User.objects.get(username = username)
				return render_to_response('dashboard/student/registration.html', {'error': 'This student already exists in our database'}, context_instance=RequestContext(request))
			except User.DoesNotExist:
				user = User.objects.create(username = username, password = surname, first_name = first_name, last_name = middle_name)
				user.is_active = False
				user.save()
				if school == 'secondary':
					student = StudentProfile.objects.create(surname = surname, address = address, admission_num = username, state = state, guardian_name = guardian_name, country = country, sex = sex, headshot = headshot, guardian_phone_number = phone, user = user)
				elif school == 'primary':
					student = PrimaryProfile.objects.create(surname = surname, address = address, admission_num = username, state = state, guardian_name = guardian_name, country = country, sex = sex, headshot = headshot, guardian_phone_number = phone, user = user)
				elif school == 'kindergarten':
					student = KindergatenProfile.objects.create(surname = surname, address = address, admission_num = username, state = state, guardian_name = guardian_name, country = country, sex = sex, headshot = headshot, guardian_phone_number = phone, user = user)
				else:
					student = PreKindergatenProfile.objects.create(surname = surname, address = address, admission_num = username, state = state, guardian_name = guardian_name, country = country, sex = sex, headshot = headshot, guardian_phone_number = phone, user = user)
				return render_to_response('dashboard/student/reg_view.html', {'student':student}, context_instance=RequestContext(request))
				
				##preview the application, with eddit button and download button
		else:
			return render_to_response('dashboard/student/registration.html', {'error': 'Oops, something went wrong'}, context_instance=RequestContext(request))
	return render_to_response('dashboard/student/registration.html', context_instance=RequestContext(request))