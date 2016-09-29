from django.db import models
from processor.models import *
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime
import PIL
from account.models import StudentProfile
from processor.models import PromotingAverage



SESSION_CHOICE = (
    ("2016/2017", "2016/2017"),
    ("2017/2018", "2018/2019"),
    ("2018/2019", "2019/2020"),
    ("2019/2020", "2020/2021"),
    ("2020/2021", "2021/2022"),
)

TERM_CHOICE = (
    ("FIRST", "FIRST"),
    ("SECOND", "SECOND"),
    ("THIRD", "THIRD"),
)

CLASS_LEVEL = (
	("JSS1", "JSS 1"),
	("JSS2", "JSS 2"),
	("JSS3", "JSS 3"),
	("SSS1", "SSS 1"),
	("SSS2", "SSS 2"),
	("SSS3", "SSS 3"),
	("PRIMARY1", "PRIMARY 1"),
	("PRIMARY2", "PRIMARY 2"),
	("PRIMARY3", "PRIMARY 3"),
	("PRIMARY4", "PRIMARY 4"),
	("PRIMARY5", "PRIMARY 5"),
	("PRIMARY6", "PRIMARY 6"),
)

ARMS_CHOICES = (
	("MARS", "MARS"),
	("PLUTO", "PLUTO"),
	("JUPITER", "JUPITER"),
	("EARTH", "EARTH"),
	("RHOMBIC", "RHOMBIC"),
	("EMERALD", "EMERALD"),
	("SATURN", "SATURN"),
	("NEPTUNE", "NEPTUNE"),
	("TRIGO", "TRIGO"),
	("TOPAZ", "TOPAZ"),
	("SCIENCE", "SCIENCE"),
	("ART", "ART"),
)

SUBJECTS_CHOICES = (
    ("Mathematics", "Mathematics"),
    ("English Language", "English Language"),
    ('Physics', 'Physics'),
    ('Chemistry', 'Chemistry'),
    ('Biology', 'Biology'),
    ('Economics', 'Economics'),
    ('Geography', 'Geography'),
    ('Igbo Lang.', 'Igbo Lang'),
    ("Creative Art", "Creative Art"),
    ("Moral Instr.", "Moral Instr."),
    ('Business Stud.', 'Business Stud.'),
    ('French Lang.', 'French Lang.'),
    ('Music', 'Music'),
    ('Commerce', 'Commerce'),
    ('Government', 'Government'),
    ('Catering & Craft Prac.', 'Catering & Craft Prac.'),
    ('Food and Nut.', 'Food and Nut.'),
    ('Animal Husbandry', 'Animal Husbandry'),
    ('Lit. in English', 'Lit. in English'),
    ('Accounting', 'Accounting'),
    ('Religious and Nat. V', 'Religious and Natural Values'),
    ('C.R.S', 'C.R.S'),
    ('Social Studies', "Social Studies"),
    ('Civic Edu.', 'Civic Edu.'),
    ('Vocation', 'Vocation'),
    ('Basic Tech.', 'Basic Tech'),
    ('P.H.E', 'P.H.E'),
    ('Basic Sci.', "Basic Sci."),
    ('Computer Sci.', 'Computer Sci.'),
    ('Pre Vocation', 'Pre Vocation'),   
    ('Home Econs', 'Home Econs'),
    ('Agric. Sci', 'Agric. Sci'),
)

VERDICT_CHOICES = (
    ("PROMOTED", "PROMOTED"),
    ("REPEAT", "REPEAT"),
)

	
class Result(models.Model):
	student = models.ForeignKey(StudentProfile)
	session = models.CharField(max_length=14, choices=SESSION_CHOICE)
	level = models.CharField(max_length=10, choices=CLASS_LEVEL, blank = True)
	term = models.CharField(max_length=10, choices=TERM_CHOICE)
	class_arm = models.CharField(max_length=10, choices=ARMS_CHOICES, blank = True)
	subject = models.CharField(max_length=50, choices=SUBJECTS_CHOICES)
	first_CA_score = models.IntegerField()
	second_CA_score = models.IntegerField()
	exam_score = models.IntegerField()
	total_score = models.IntegerField(editable = False, default = 0)
	class_average = models.ForeignKey('SubjectAverage', editable = False, blank = True, null = True )
	grade = models.CharField(max_length=2, blank = True, editable = False)


	def __unicode__(self):
		return self.student.surname + " " + self.student.first_name

	def save(self):
		#for total score computation
		self.total_score = self.exam_score + self.first_CA_score + self.second_CA_score
		if not self.class_arm:
			self.class_arm = self.student.class_arm
		if not self.level:
			self.level = self.student.current_level
		super(Result, self).save()
		result = Result.objects.filter(student=self.student, session=self.session, level=self.level, term=self.term)
		#for the grading system for junior and senior
		if self.level == 'JSS1' or self.level =='JSS2' or self.level =='JSS3':
			if self.total_score <= 39:
				self.grade = 'F'
			elif self.total_score <= 54:
				self.grade = 'P'
			elif self.total_score <= 69:
				self.grade = 'C'
			else:
				self.grade = 'A'
			super(Result, self).save()

		#for the grading system for senior			
		else:
			if self.total_score <= 39:
				self.grade = 'F'
			elif self.total_score <= 44:
				self.grade = 'E8'
			elif self.total_score <= 49:
				self.grade = 'D7'
			elif self.total_score <= 54:
				self.grade = 'C6'
			elif self.total_score <= 59:
				self.grade = 'C5'
			elif self.total_score <= 64:
				self.grade = 'C4'
			elif self.total_score <= 69:
				self.grade = 'B3'
			elif self.total_score <= 74:
				self.grade = 'B2'
			else:
				self.grade = 'A1'
			super(Result, self).save()
		
		try:
			#if it exists
			result_summary = ResultSummary.objects.get(student=self.student,session=self.session,level= self.level, term=self.term, class_arm = self.class_arm)
		except:
			#if it doesnt exist create
			result_summary = ResultSummary(student=self.student,session=self.session,level= self.level, term=self.term, class_arm = self.class_arm)
		if len(result) == 0:
			result_summary.average = self.total_score
			result_summary.class_arm = self.class_arm
			result_summary.save()
			return
		else:
			super(Result, self).save()
			result = Result.objects.filter(student=self.student, session=self.session, level=self.level, term=self.term)
			count = 0
			sum = 0.0
			for i in result:
				sum = sum + i.total_score
				count = count + 1
			result_summary.average = sum/count
			result_summary.class_arm = self.class_arm
			result_summary.save()
			class_summary = ResultSummary.objects.filter(session=self.session, level=self.level, term=self.term, class_arm=self.class_arm)
			averages_list = []
			for j in class_summary:
				averages_list.append(j.average)
				averages_list.sort(reverse=True)
				position = averages_list.index(j.average)
				position = position + 1
				j.position = str(position)
				j.save()

		result_an = Result.objects.filter(student = self.student, session = self.session, level = self.level)
		try:
			annual_summary = AnnualSummary.objects.get(student=self.student, session=self.session, level= self.level, class_arm = self.class_arm)
		except:
			annual_summary = AnnualSummary(student=self.student, session=self.session, level= self.level, class_arm = self.class_arm)
		if len(result_an) == 0:
			annual_summary.average = self.total_score
			annual_summary.class_arm = self.class_arm
			annual_summary.save()
			#super(Result, self).save()
			return
		else:
			super(Result, self).save()
			count = 0
			sum = 0.0
			for i in result_an:
				sum = sum + i.total_score
				count = count + 1
			annual_summary.average = sum/count
			annual_summary.class_arm = self.class_arm
			annual_summary.save()
			annual_summaryz = AnnualSummary.objects.filter(session=self.session, level=self.level, class_arm=self.class_arm)
			averages_list = []
			for j in annual_summaryz:
				averages_list.append(j.average)
				averages_list.sort(reverse=True)
				position = averages_list.index(j.average)
				position = position + 1
				j.position = str(position)
				j.save()
				
		try:
			subav = SubjectAverage.objects.get(session=self.session, level= self.level, subject = self.subject, class_arm = self.class_arm, term = self.term)
		except:
			subav = SubjectAverage(session=self.session, level= self.level, subject = self.subject, class_arm = self.class_arm)
		res_sub = Result.objects.filter(session = self.session, level = self.level, term = self.term, subject = self.subject, class_arm = self.class_arm)
		count = 0
		sum = 0.0
		for i in res_sub:
			sum = sum + i.total_score
			count = count + 1
		subav.average = sum/count
		subav.class_arm = self.class_arm

		subav.save()

		#ABB = SubjectAverage.objects.get(session=self.session, level= self.level, subject = self.subject, class_arm = self.class_arm)
		self.class_average = subav
		super(Result, self).save()

		try:
			result_annual = Annual.objects.get(student=self.student, session=self.session, level= self.level, subject = self.subject)
		except:
			result_annual = Annual(student=self.student, session=self.session, level= self.level, subject = self.subject)
		result_sub = Result.objects.filter(student=self.student, session=self.session, level=self.level, subject = self.subject)
		count = 0
		sum = 0.0
		esum = 0.0
		csum = 0.0
		dsum = 0.0
		for i in result_sub:
			sum = sum + i.total_score
			csum = csum + i.first_CA_score
			dsum = dsum + i.second_CA_score
			esum = esum + i.exam_score
			count = count + 1
		result_annual.total_score = sum/count
		result_annual.first_CA_score = csum/count
		result_annual.second_CA_score = dsum/count
		result_annual.exam_score = esum/count
		result_annual.class_arm = self.class_arm
		result_annual.save()
		

class ResultSummary(models.Model):
	student = models.ForeignKey(StudentProfile)
	session = models.CharField(max_length=14)
	level = models.CharField(max_length=10)
	term = models.CharField(max_length=7)
	class_arm = models.CharField(max_length=10)
	average = models.DecimalField(decimal_places=2, max_digits=5)
	position = models.CharField(max_length=3)
	comment = models.CharField(max_length=400, blank=True)
	publish = models.BooleanField(default = False)

	def __unicode__(self):
		return self.student.admission_num + " " + self.session
		

	class Meta:
		ordering = ["-session", "level", "-average", "position"]
		verbose_name = "Result Summary for individual students"
		verbose_name_plural = "Result summaries"
		

class SubjectAverage(models.Model):
	session = models.CharField(max_length=14)
	term = models.CharField(max_length=10, choices=TERM_CHOICE)
	subject = models.CharField(max_length=50, choices=SUBJECTS_CHOICES)
	level = models.CharField(max_length=10)
	class_arm = models.CharField(max_length=10)
	average = models.DecimalField(decimal_places=2, max_digits=5)

	def __unicode__(self):
		return str(self.average)
	
		
class Annual(models.Model):
	student = models.ForeignKey(StudentProfile)
	session = models.CharField(max_length=14, choices=SESSION_CHOICE)
	level = models.CharField(max_length=10, choices=CLASS_LEVEL)
	class_arm = models.CharField(max_length=10)
	subject = models.CharField(max_length=50, choices=SUBJECTS_CHOICES)
	first_CA_score = models.DecimalField(decimal_places=2, max_digits=5)
	second_CA_score = models.DecimalField(decimal_places=2, max_digits=5)
	exam_score = models.DecimalField(decimal_places=2, max_digits=5)
	total_score = models.DecimalField(decimal_places=2, max_digits=5)
	class_average = models.DecimalField(decimal_places=2, max_digits=5, null = True)
	grade = models.CharField(max_length=2, blank = True, editable = False)

	def __unicode__(self):
		return self.student.surname + " " + self.student.first_name

	def save(self):
		#for the grading system for junior and senior
		if self.level == 'JSS1' or self.level =='JSS2' or self.level =='JSS3':
			if self.total_score <= 39:
				self.grade = 'F'
			elif self.total_score <= 54:
				self.grade = 'P'
			elif self.total_score <= 69:
				self.grade = 'C'
			else:
				self.grade = 'A'
			super(Annual, self).save()

		#for the grading system for senior			
		else:
			if self.total_score <= 39:
				self.grade = 'F'
			elif self.total_score <= 44:
				self.grade = 'E8'
			elif self.total_score <= 49:
				self.grade = 'D7'
			elif self.total_score <= 54:
				self.grade = 'C6'
			elif self.total_score <= 59:
				self.grade = 'C5'
			elif self.total_score <= 64:
				self.grade = 'C4'
			elif self.total_score <= 69:
				self.grade = 'B3'
			elif self.total_score <= 74:
				self.grade = 'B2'
			else:
				self.grade = 'A1'
			super(Annual, self).save()
			
		subav = SubjectAverage.objects.filter(session = self.session, level = self.level, subject = self.subject, class_arm = self.class_arm)
		count = 0.0
		sum = 0.0
		for i in subav:
			sum = float(sum) + float(i.average)
			count = count + 1.0
		self.class_average = sum/float(count)
		super(Annual, self).save()

	
	
class AnnualSummary(models.Model):
	student = models.ForeignKey(StudentProfile)
	session = models.CharField(max_length=14)
	level = models.CharField(max_length=10)
	class_arm = models.CharField(max_length=10)
	average = models.DecimalField(decimal_places=2, max_digits=5)
	position = models.CharField(max_length=3)
	verdict = models.CharField(max_length=15,choices=VERDICT_CHOICES, default="Promoted", editable = False)

	def __unicode__(self):
		return self.student.surname + " " + self.student.first_name
		
	def save(self):
		try:
			mark = PromotingAverage.objects.get(session = self.session, level = self.level)
			if self.average < mark.passmark:
				self.verdict = "Repeat"
			else:
				self.verdict = "Promoted"
			super(AnnualSummary, self).save()
		except:
			pass
			super(AnnualSummary, self).save()
