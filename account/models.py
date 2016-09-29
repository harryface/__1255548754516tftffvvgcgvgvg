from django.db import models
from processor.models import *
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime
import PIL
from resultprocessor.models import *

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

SUBJECTS_CHOICES = (
    ("Mathematics", "Mathematics"),
    ("English Lang.", "English Lang"),
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

SEX = (
	("MALE", "MALE"),
	("FEMALE", "FEMALE"),
)

ARMS_CHOICES = (
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
    ("F", "F"),
    ("G", "G"),
    ("H", "H"),
)
SESSION_CHOICE = (
    ("2016/2017", "2016/2017"),
    ("2017/2018", "2018/2019"),
    ("2018/2019", "2019/2020"),
    ("2019/2020", "2020/2021"),
    ("2020/2021", "2021/2022"),
)

class AdminProfile(models.Model):
	user = models.ForeignKey(User, unique = True)
	surname = models.CharField(max_length=40, blank = True)
	first_name = models.CharField(max_length=40, blank = True)
	middle_name = models.CharField(max_length=40, blank = True)
	address = models.CharField(max_length=100, blank = True)
	state_of_origin = models.CharField(max_length=50, blank=True)
	address = models.CharField(max_length=100, blank=True)
	country = models.CharField(max_length=40, blank = True)
	sex = models.CharField(max_length=40, blank = True, choices = SEX)
	mobile_phone = models.CharField(max_length=40, blank = True)
	headshot = models.ImageField(upload_to = 'static/photos')
	date_of_registration = models.DateTimeField(auto_now_add=True, editable = False)


	def __str__(self):
		return self.user.username + " | Admin"
	

class CbtProfile(models.Model):
	user = models.ForeignKey(User, blank = True, null = True)
	reg_number = models.CharField(max_length=40)
	surname = models.CharField(max_length=40)
	e_mail = models.EmailField()
	first_name = models.CharField(max_length=40)
	middle_name = models.CharField(max_length=40, blank = True)
	address = models.CharField(max_length=100, blank = True)
	state_of_origin = models.CharField(max_length=50, blank=True)
	local_govt_of_origin = models.CharField(max_length=50, blank=True)
	home_address = models.CharField(max_length=100, blank=True)
	country = models.CharField(max_length=40, blank = True)
	sex = models.CharField(max_length=40, blank = True, choices = SEX)
	mobile_phone = models.CharField(max_length=40, blank = True)
	headshot = models.ImageField(upload_to = 'static/photos')
	date_of_registration = models.DateTimeField(auto_now_add=True, editable = False)
	
	def save(self):
		try:
			a = CbtProfile.objects.get(pk = self.pk)
			if a.headshot != self.headshot:
				a.headshot.delete(save=False)
			self.headshot = self.headshot
		except:
			u = User.objects.create(username = self.reg_number, password = self.surname, first_name = self.first_name, last_name = self.surname)
			u.save()
			self.user = u
		super(CbtProfile, self).save()
		

class Student(models.Model):
	user = models.ForeignKey(User, unique = True)
	surname = models.CharField(max_length=40, blank = True)
	first_name = models.CharField(max_length=50)
	middle_name = models.CharField(max_length=30, blank=True)
	admission_num = models.CharField(max_length=40, blank = True)
	address = models.CharField(max_length=100, blank = True)
	state = models.CharField(max_length=50, blank=True)
	local_govt_of_origin = models.CharField(max_length=50, blank=True)
	home_address = models.CharField(max_length=100, blank=True)
	country = models.CharField(max_length=40, blank = True)
	birthday = models.DateField(blank = True, null = True)
	sex = models.CharField(max_length=40, blank = True, choices = SEX)
	mobile_phone = models.CharField(max_length=40, blank = True)
	headshot = models.ImageField(upload_to = 'static/photos')
	guardian_name = models.CharField(max_length=50, blank=True)
	guardian_phone_number = models.CharField(max_length=15)
	activated = models.BooleanField (default = False)
	graduated = models.BooleanField (default = False)
	date_of_registration = models.DateTimeField(auto_now_add=True, editable = False)

	"""def save(self):
		
		if self.activated == True:
			self.user.is_active = True
		else:
			self.user.is_active = False

		super(Student, self).save()
	"""	
	def __str__(self):
		return self.user.username + " | " + self.admission_num
	
	def delete(self):
		user = User.objects.get(username = self.admission_num)
		user.delete()
		super(Student, self).delete()
		
		
class StudentProfile (Student):
	level = models.CharField(max_length=10, choices=CLASS_LEVEL, blank = True)
	class_arm = models.CharField(max_length=1, choices=ARMS_CHOICES, blank = True)
	
		
class PrimaryProfile (Student):
	level = models.CharField(max_length=10, choices=CLASS_LEVEL, blank = True)
	class_arm = models.CharField(max_length=1, choices=ARMS_CHOICES, blank = True)
	
		
class KindergatenProfile (Student):
	level = models.CharField(max_length=10, choices=CLASS_LEVEL, blank = True)
	class_arm = models.CharField(max_length=1, choices=ARMS_CHOICES, blank = True)
	
		
class PreKindergatenProfile (Student):
	level = models.CharField(max_length=10, choices=CLASS_LEVEL, blank = True)
	class_arm = models.CharField(max_length=1, choices=ARMS_CHOICES, blank = True)
	

class ClassGroup (models.Model):
	student = models.ManyToManyField(StudentProfile)
	session = models.CharField(max_length=14, choices=SESSION_CHOICE)
	level = models.CharField(max_length=10, choices=CLASS_LEVEL, blank = True)
	class_arm = models.CharField(max_length=1, choices=ARMS_CHOICES, blank = True)
