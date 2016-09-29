from django.db import models
from processor.models import *
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime
import PIL
from account.modeels import *

	
class Mathematics(models.Model):
	student = models.ForeignKey(KindergatenProfile)
	a = models.IntegerField(default=0)
	a_comment = models.CharField(max_length=30)
	b = models.IntegerField(default=0)
	b_comment = models.CharField(max_length=30)
	c = models.IntegerField(default=0)
	c_comment = models.CharField(max_length=30)
	d = models.IntegerField(default=0)
	d_comment = models.CharField(max_length=30)
	percentage = models.IntegerField(default=0)
	
	def save(self):
		#for total score computation
		total = self.a + self.b + self.c + self.d
		self.percentage = (total * 100) / 400
		
		super(Mathematics, self).save()
		
class Language(models.Model):
	student = models.ForeignKey(KindergatenProfile)
	a = models.IntegerField(default=0)
	a_comment = models.CharField(max_length=30)
	b = models.IntegerField(default=0)
	b_comment = models.CharField(max_length=30)
	c = models.IntegerField(default=0)
	c_comment = models.CharField(max_length=30)
	d = models.IntegerField(default=0)
	d_comment = models.CharField(max_length=30)
	e = models.IntegerField(default=0)
	e_comment = models.CharField(max_length=30)
	f = models.IntegerField(default=0)
	f_comment = models.CharField(max_length=30)
	g = models.IntegerField(default=0)
	g_comment = models.CharField(max_length=30)
	percentage = models.IntegerField(default=0)
	
	def save(self):
		#for total score computation
		total = self.a + self.b + self.c + self.d + self.e + self.f + self.g
		self.percentage = (total * 100) / 700
		
		super(Language, self).save()
		
		
class WordStudy(models.Model):
	student = models.ForeignKey(KindergatenProfile)
	a = models.IntegerField(default=0)
	a_comment = models.CharField(max_length=30)
	b = models.IntegerField(default=0)
	b_comment = models.CharField(max_length=30)
	c = models.IntegerField(default=0)
	c_comment = models.CharField(max_length=30)
	percentage = models.IntegerField(default=0)
	
	def save(self):
		#for total score computation
		total = self.a + self.b + self.c
		self.percentage = (total * 100) / 300
		
		super(WordStudy, self).save()
		
class PhonicSkill(models.Model):
	student = models.ForeignKey(KindergatenProfile)
	a = models.IntegerField(default=0)
	a_comment = models.CharField(max_length=30)
	b = models.IntegerField(default=0)
	b_comment = models.CharField(max_length=30)
	c = models.IntegerField(default=0)
	c_comment = models.CharField(max_length=30)
	d = models.IntegerField(default=0)
	d_comment = models.CharField(max_length=30)
	e = models.IntegerField(default=0)
	e_comment = models.CharField(max_length=30)
	f = models.IntegerField(default=0)
	f_comment = models.CharField(max_length=30)
	
	def save(self):
		#for total score computation
		total = self.a + self.b + self.c + self.d + self.e + self.f
		self.percentage = (total * 100) / 600
		
		super(PhonicSkill, self).save()
		
		
class WritingSkill(models.Model):
	student = models.ForeignKey(KindergatenProfile)
	a = models.IntegerField(default=0)
	a_comment = models.CharField(max_length=30)
	b = models.IntegerField(default=0)
	b_comment = models.CharField(max_length=30)
	c = models.IntegerField(default=0)
	c_comment = models.CharField(max_length=30)
	d = models.IntegerField(default=0)
	d_comment = models.CharField(max_length=30)
	e = models.IntegerField(default=0)
	e_comment = models.CharField(max_length=30)
	
	def save(self):
		#for total score computation
		total = self.a + self.b + self.c + self.d + self.e
		self.percentage = (total * 100) / 500
		
		super(WritingSkill, self).save()
		
		
class Ple(models.Model):
	student = models.ForeignKey(KindergatenProfile)
	a = models.IntegerField(default=0)
	a_comment = models.CharField(max_length=30)
	b = models.IntegerField(default=0)
	b_comment = models.CharField(max_length=30)
	c = models.IntegerField(default=0)
	c_comment = models.CharField(max_length=30)
	d = models.IntegerField(default=0)
	d_comment = models.CharField(max_length=30)
	e = models.IntegerField(default=0)
	e_comment = models.CharField(max_length=30)
	f = models.IntegerField(default=0)
	f_comment = models.CharField(max_length=30)
	g = models.IntegerField(default=0)
	g_comment = models.CharField(max_length=30)
	h = models.IntegerField(default=0)
	h_comment = models.CharField(max_length=30)
	i = models.IntegerField(default=0)
	i_comment = models.CharField(max_length=30)
	j = models.IntegerField(default=0)
	j_comment = models.CharField(max_length=30)
	k = models.IntegerField(default=0)
	k_comment = models.CharField(max_length=30)
	l = models.IntegerField(default=0)
	l_comment = models.CharField(max_length=30)
	m = models.IntegerField(default=0)
	m_comment = models.CharField(max_length=30)
	n = models.IntegerField(default=0)
	n_comment = models.CharField(max_length=30)
	o = models.IntegerField(default=0)
	o_comment = models.CharField(max_length=30)
	p = models.IntegerField(default=0)
	p_comment = models.CharField(max_length=30)
	
	def save(self):
		#for total score computation
		total = self.a + self.b + self.c + self.d + self.e + self.f + self.g + self.h + self.i + self.j + self.k + self.l + self.m + self.n + self.o + self.p
		self.percentage = (total * 100) / 1600
		
		super(Ple, self).save()
		
		
class Sensorial(models.Model):
	student = models.ForeignKey(KindergatenProfile)
	a = models.IntegerField(default=0)
	a_comment = models.CharField(max_length=30)
	b = models.IntegerField(default=0)
	b_comment = models.CharField(max_length=30)
	c = models.IntegerField(default=0)
	c_comment = models.CharField(max_length=30)
	d = models.IntegerField(default=0)
	d_comment = models.CharField(max_length=30)
	e = models.IntegerField(default=0)
	e_comment = models.CharField(max_length=30)
	f = models.IntegerField(default=0)
	f_comment = models.CharField(max_length=30)
	g = models.IntegerField(default=0)
	g_comment = models.CharField(max_length=30)
	h = models.IntegerField(default=0)
	h_comment = models.CharField(max_length=30)
	
	
	def save(self):
		#for total score computation
		total = self.a + self.b + self.c + self.d + self.e + self.f + self.g + self.h
		self.percentage = (total * 100) / 800
		
		super(Sensorial, self).save()
		
		
class GeneralPaper(models.Model):
	student = models.ForeignKey(KindergatenProfile)
	a = models.IntegerField(default=0)
	a_comment = models.CharField(max_length=30)
	b = models.IntegerField(default=0)
	b_comment = models.CharField(max_length=30)
	c = models.IntegerField(default=0)
	c_comment = models.CharField(max_length=30)
	d = models.IntegerField(default=0)
	d_comment = models.CharField(max_length=30)
	
	
	def save(self):
		#for total score computation
		total = self.a + self.b + self.c + self.d
		self.percentage = (total * 100) / 400
		
		super(GeneralPaper, self).save()
		
		
class Subject(models.Model):
	student = models.ForeignKey(KindergatenProfile)
	physical_education = models.IntegerField(default=0)
	physical_education_comment = models.CharField(max_length=30)
	civic_education = models.IntegerField(default=0)
	civic_education_comment = models.CharField(max_length=30)
	french = models.IntegerField(default=0)
	french_comment = models.CharField(max_length=30)
	music = models.IntegerField(default=0)
	music_comment = models.CharField(max_length=30)
	art = models.IntegerField(default=0)
	art_comment = models.CharField(max_length=30)
	igbo = models.IntegerField(default=0)
	igbo_comment = models.CharField(max_length=30)
	
	
	def save(self):
		#for total score computation
		total = self.a + self.b + self.c + self.d + self.e + self.f 
		self.percentage = (total * 100) / 600
		
		super(Subject, self).save()
		
		
class Courtesy(models.Model):
	student = models.ForeignKey(KindergatenProfile)
	a = models.IntegerField(default=0)
	a_comment = models.CharField(max_length=30)
	b = models.IntegerField(default=0)
	b_comment = models.CharField(max_length=30)
	c = models.IntegerField(default=0)
	c_comment = models.CharField(max_length=30)
	d = models.IntegerField(default=0)
	d_comment = models.CharField(max_length=30)
	e = models.IntegerField(default=0)
	e_comment = models.CharField(max_length=30)
	f = models.IntegerField(default=0)
	f_comment = models.CharField(max_length=30)
	g = models.IntegerField(default=0)
	g_comment = models.CharField(max_length=30)
	
	
	def save(self):
		#for total score computation
		total = self.a + self.b + self.c + self.d + self.e + self.f + self.g
		self.percentage = (total * 100) / 800
		
		super(Courtesy, self).save()
		
		
class ProjectWork (models.Model):
	student = models.ForeignKey(KindergatenProfile)
	topic = models.CharField(max_length=300)
	level_of_participation = models.CharField(max_length=300)
	grade = models.CharField(max_length=3)
	parent_participation = models.CharField(max_length=100)
	
	
class WalkOnLine(models.Model):
	student = models.ForeignKey(KindergatenProfile)
	a = models.IntegerField(default=0)
	a_comment = models.CharField(max_length=30)
	b = models.IntegerField(default=0)
	b_comment = models.CharField(max_length=30)
	c = models.IntegerField(default=0)
	c_comment = models.CharField(max_length=30)
	d = models.IntegerField(default=0)
	d_comment = models.CharField(max_length=30)
		
	
	def save(self):
		#for total score computation
		total = self.a + self.b + self.c + self.d
		self.percentage = (total * 100) / 400
		
		super(WalkOnLine, self).save()
		
		
class Comment (models.Model):
	student = models.ForeignKey(KindergatenProfile)
	teacher_comment = models.CharField(max_length=300)
	teacher_name = models.CharField(max_length=300)
	principal_comment = models.CharField(max_length=300)
	principal_name = models.CharField(max_length=300)
	hod_name =  models.CharField(max_length=300)
	hod_comment =  models.CharField(max_length=300)
	verdit =  models.CharField(max_length=300)
	#date = 
	