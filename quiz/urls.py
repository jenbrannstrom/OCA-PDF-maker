"""quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from quizapp import views
from django.views.generic.base import TemplateView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',TemplateView.as_view(template_name='home.html'), name="registeration"),
    path('',views.RegisterView.as_view(), name="registeration"),

    path('detail/',views.DetailUserView.as_view(),name='user_detail'),
    url(r'survey/(?P<id>\d+)/$',views.DetailResultView.as_view(),name='survey_detail'),

    path('quiz/',TemplateView.as_view(template_name='scientogy.html'),name='quiz'),
    path('quiz/ques/',views.QuestionView.as_view(), name='questions'),    
    url(r'quiz/(?P<id>\d+)/(?P<value>\w+)/$', views.loadNextQuestion, name='next_page'),
    url(r'quiz/next/(?P<id>\d+)/$', views.nextQuestion, name='next_ques'),
    url(r'quiz/prev/(?P<id>\d+)/$', views.previousQuestion, name='prev_ques'),

    # path('question/',views.addQuestions,name="add_question"),
    # url(r'completion/', views.CompletionView.as_view(), name='complete'),
    url(r'completion/(?P<value>\w+)/$', views.CompletionView.as_view(), name='complete'),

    url(r'result/(?P<value>\w+)/$', views.GenerateResult.as_view(), name='result'),    
    # url(r'result/(?P<id>\d+)/$', views.GenerateResult.as_view(), name='result'),     
    path('privacy/',views.PrivacyView.as_view(),name='privacy'),
    path('cookie/',views.CookieView.as_view(),name='cookie'),
    path('leagal/',views.LeagalView.as_view(),name='leagal'),
    path('terms/',views.TermsView.as_view(),name='terms'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
