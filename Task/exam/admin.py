from django.contrib import admin

from .models import Choice, Question, Course, Chapter

# Register your models here.

admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Chapter)
admin.site.register(Course)
