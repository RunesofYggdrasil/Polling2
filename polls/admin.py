from django.contrib import admin
from django.http import JsonResponse
from . models import Question, Choice, Vote

# Register your models here.

admin.site.site_header = "Admin/Controller"
admin.site.site_title = "Admin Area"
admin.site.index_title = 'Please finalise everything before publishing'

class ChoiceInLine(admin.TabularInline):  # Or use admin.StackedInline for a different layout
    model = Choice
    extra = 0 #admin still will have option to add options, blank spaces will just not be shown by default

class QuestionAdmin(admin.ModelAdmin): #what will be displayed on admin post login
    fieldsets = [('View menu and vote for what you want!', {'fields': ['question_text']}), 
              ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),] #latter enables to collapse
    
    inlines = [ChoiceInLine] #enables admin to edit choices

    list_display = ('question_text', 'pub_date')

    list_filter = ['pub_date'] 

    search_fields = ['choice_text'] #can search among choices to see if desired item is there(and if user is lazy)

    def get_readonly_fields(self, request, obj=None): #request refer to http req, obj= none if we want to edit new question
        if obj:
            return ['pub_date']
        return [] #all questions editable

    actions = ['export_as_json'] #actions is an attribute of an Admin class, here this 'custom action' allows us to export selected questions as JSON data

    def export_as_json(self, request, queryset): #queryset goes through questions selected by admin
        data = []
        for question in queryset:
            data.append({
                "model": "polls.question",
                "pk": question.pk, #pk here+mentioned in json file because Django key word
                "fields": {
                    "question_text": question.question_text,
                    "pub_date": question.pub_date.isoformat(), #typa string for JSON timestamps
                }
            })
        return JsonResponse(data, safe=False) #helper function, Django's inbuilt
    
    export_as_json.short_description = "Export selected questions as JSON"


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Vote)