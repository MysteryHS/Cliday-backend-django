from django.contrib import admin

from .models import Account, Question, Answer, Choice, Category

admin.site.register(Account)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Choice)
admin.site.register(Category)