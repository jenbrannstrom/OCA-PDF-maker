from django.contrib import admin
from quizapp.models import Question, Answer, Profile

# Register your models here.
admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Answer)