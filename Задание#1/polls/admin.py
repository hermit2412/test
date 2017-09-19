from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

    """
    Переписываем get_readonly_fields используя метод choice_state_check
    из модуля models для получения списка полей которые должны быть read only.
    """
    def get_readonly_fields(self,request,obj):
        if obj == None:
            return super(ChoiceInline,self).readonly_fields
        if obj.state == 'F':
            self.can_delete = False
        return obj.choice_state_check()


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('State', {'fields':['state']})
    ]
    inlines = [ChoiceInline]
    list_display = ['question_text','pub_date', 'was_published_recently','state',]
    list_editable = ['state']
    list_filter = ['pub_date']
    search_fields = ['question_text']
    actions = ['make_new']

    """
    Переписываем get_readonly_fields используя метод question_state_check
    из модуля models для получения списка полей которые должны быть read only.
    """
    def get_readonly_fields(self,request,obj):
        if obj == None:
            return super(QuestionAdmin,self).readonly_fields
        return obj.question_state_check()


admin.site.register(Question, QuestionAdmin)
