from django.db import models
from resultprocessor.models import *
from account.models import *


STATUS_CHOICES = (
	('PUBLISHED', 'PUBLISHED'),
)

class Card(models.Model):
	pin = models.BigIntegerField(unique = True, editable = False)
	time_created = models.DateTimeField(auto_now_add=True)
	session = models.CharField("Session Used In", max_length = 8, editable = False, blank=True)
	term = models.CharField("Term Used In", max_length = 8, editable = False, blank=True)
	arm = models.CharField("Term Used In", max_length = 8, editable = False, blank=True)
	num_used = models.IntegerField(default = 0, blank=True, editable = False)
	user = models.ForeignKey(StudentProfile, blank=True, null=True, editable = False, verbose_name = "Used By")
	level = models.CharField("Class Used On", max_length = 8, editable = False, blank=True)
	
	
	def __unicode__(self):
		return str(self.pin)
	

class PromotingAverage (models.Model):
    session = models.CharField(max_length=14, choices=SESSION_CHOICE)
    level = models.CharField(max_length=10, choices=CLASS_LEVEL)
    passmark = models.IntegerField(default = 50)

    def __unicode__(self):
        return self.level + " " + str(self.passmark)

    def save(self):
        try:
            promotingaverage = PromotingAverage.objects.filter(session = self.session, level = self.level)
            promotingaverage.delete()
            super(PromotingAverage, self).save()
        except:
            pass
        try:
            annual_summary = AnnualSummary.objects.filter(session = self.session, level = self.level)
            for item in annual_summary:
                item.save()
            super(PromotingAverage, self).save()
        except:
            pass
            super(PromotingAverage, self).save()
			
    class Meta:
        verbose_name_plural = "Set Promotion Average"
		

class Message (models.Model):
	sender_id = models.CharField(max_length=14)
	phone_numbers = models.TextField()
	message_body = models.TextField()
	date_sent = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=12)
	
	def __unicode__(self):
		return self.sender_id
