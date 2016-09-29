from django.contrib import admin
from resultprocessor.models import *
from processor.models import *
from blog.models import *
from account.models import *
from resultsheet.models import *
import csv
from django.http import HttpResponse


admin.site.register(AdminProfile)
###############################################################################################################
class ResultInline(admin.TabularInline):
	model = Result
	can_delete = False
	
class ClassGroupAdmin(admin.ModelAdmin):
	list_display = ['session', 'level', 'class_arm', 'publish_results']
	#list_display = ['student', 'session', 'first_CA_score', 'second_CA_score', 'exam_score', 'total_score', 'grade', 'class_average']
	list_filter = ['session', 'level', 'class_arm']
	inlines = (ResultInline, )
	
		
	"""def get_name(self, obj):
		return obj.student.surname
		get_name.admin_order_field  = 'student'  #Allows column order sorting
		get_name.short_description = 'Student Name'  #Renames column head"""
	
#admin.site.register(ClassGroup, ClassGroupAdmin)

################################################################################################################
	

class StudentAdmin(admin.ModelAdmin):
	inlines = (ResultInline, )
	list_display = ['surname', 'first_name', 'middle_name', 'admission_num']
	search_fields = ["admission_num", "surname"]
	fieldsets = (
		(None, {'fields': ('surname', 'first_name', 'middle_name', 'admission_num', 'headshot')}),
		('More options', {'classes': ('collapse',),'fields': ('guardian_name', 'guardian_phone_number')}),)

admin.site.register(StudentProfile, StudentAdmin)

################################################################################################################
	

	
class CardAdmin(admin.ModelAdmin):
	list_display = ['pin', 'user', 'num_used', 'session', 'level', 'term', 'time_created']
	
admin.site.register(Card, CardAdmin)

	
class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    display_fields = ["title", "created"]
	
admin.site.register(Post, PostAdmin)


class ResultAdmin(admin.ModelAdmin):
	list_display = ['student', 'session', 'first_CA_score', 'second_CA_score', 'subject', 'exam_score', 'total_score', 'grade', 'class_average']
	list_filter = ['session', 'level', 'class_arm']
	
admin.site.register(Result, ResultAdmin)

	
class ResultSummaryAdmin(admin.ModelAdmin):
	list_display = ['session', 'student', 'level','class_arm', 'term', 'average', 'position']
	actions = ['download_csv']
	
	def download_csv (self, request, queryset):
		response = HttpResponse(mimetype='text/csv')
		response['Content-Disposition'] = 'attachment; filename=stat.csv'

		writer = csv.writer(response)
		writer.writerow(['session', 'student', 'level','class_arm', 'term', 'average', 'position', 'publish'])
		for obj in queryset:
			writer.writerow([getattr(obj, field) for field in ('session', 'student', 'level','class_arm', 'term', 'average', 'position')])
		return response
		
		download_csv.short_description = "Download CSV file for selected stats."
	
admin.site.register(ResultSummary, ResultSummaryAdmin)

	
class PromotingAverageAdmin(admin.ModelAdmin):
	list_display = ["session", "level", "passmark"]
	
admin.site.register(PromotingAverage, PromotingAverageAdmin)


class MessageAdmin(admin.ModelAdmin):
	list_display = ['sender_id', 'phone_numbers', 'message_body', 'status', 'date_sent']
	
admin.site.register(Message, MessageAdmin)
#admin.site.register()

admin.site.register(KgSheet)
