import os
import json
from datetime import date
import datetime
from bs4 import BeautifulSoup
import requests

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from quizapp.models import Question, Answer, Profile
from django.views.generic.base import TemplateView
from django.views import View
from django.core import serializers

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string, get_template

from django.core.mail import send_mail
from django.conf import settings
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
import tempfile
from django.core.mail import EmailMessage
from django.conf import settings

class GenerateResult(View):

	def get(self, request, *args, **kwargs):
		status = ""
		if self.kwargs['value']:
			print("self.kwargs['value'] ==> ", self.kwargs['value'])
			status = self.kwargs['value']		

		user = Profile.objects.latest('id')
		# print(user,'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
		answers = Answer.objects.filter(user=user.id)
		# print("user.id ==> ", user.id)
		# print("Answer ==> ", answers)
		# print("Answer ==> ", answers[0].answer)
		# print("Answer ==> ", answers[0].question)
		
		font_config = FontConfiguration()
		date = datetime.datetime.today().date()
		time = datetime.datetime.today().time()
		# print("date ==> ", date)
		# print("time ==> ", time)

		pdf_string = render_to_string('pdf.html', locals())
		
		html = HTML(string= pdf_string, base_url=request.build_absolute_uri()) 
				
		pdf_file = html.write_pdf(target="/tmp/"+user.firstname+'_result.pdf',  font_config=font_config)

		print(" ********** PDF Generated ************** ")


		
		subject = "Survey Result email !!"
		recipients = ['jen@rtb.cat ','redexsolutionspvtlmt@gmail.com', 'ocatampabay@gmail.com', 'meenuaviox@gmail.com'] #'auditoryen@gmail.com'] #[user.email]
		message = "" 
		if(len(answers)<200): #200
			if status == "inactivity":  
				message = user.firstname +" was inactive for 10 minutes, Here are the answers gotten"
			if status == "quit":
				message = user.firstname +" did not complete the survey with 200 questions and quit the survey in between."	#200	
		else:
			message = user.firstname +" completed the survey with 200 questions." #200


		try:

			# file = open( './' +user.firstname+'_result.pdf', "rb")
			mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipients)
			mail.attach_file("/tmp/"+user.firstname+'_result.pdf') 
			mail.send()			
		except Exception as e:
			print(str(e))
			raise e
		return HttpResponseRedirect('/completion/')



class DetailUserView(TemplateView):
	template_name = "user_detail.html"	

	def get(self, request, *args, **kwargs):

		try:
			superuser = request.user		
			print("User ==> ", superuser)

			if superuser.is_authenticated & superuser.is_superuser:
				print("Authenticated username => ", superuser.username)
				users = Profile.objects.all()

				return render(request, self.template_name, {"Status":"Success", "superuser":superuser ,'users':users})
				
			else:
				print("Anonymous user")
				return render(request, self.template_name, {})
		except Exception as e:
			raise e



class DetailResultView(TemplateView):
	template_name = "detail.html"	

	def get(self, request, *args, **kwargs):
		user_id = self.kwargs['id']
		questions = Question.objects.all()
		user = Profile.objects.get(id=user_id)
		answers = Answer.objects.filter(user=user.id)
		
		# font_config = FontConfiguration()
		# date = datetime.datetime.today().date()
		# time = datetime.datetime.today().time()
		

		return render(request, self.template_name, {"Status":"Success", 'user': user, 'questions':questions , 'answers':answers}) #'date':date,'time':time, 'answers':answers})
		

#Register user
class RegisterView(TemplateView):
	# template_name =  "pdf.html" 
	template_name =  "home.html" 

	def get(self, request, *args, **kwargs):

		# user = Profile.objects.get(id=71)
		# print("user id ==> ", user.id)

		# # user = Profile.objects.latest('id')
		# answers = Answer.objects.filter(user=user.id)
		
		# print("Answer ==> ", answers)		
		
		# date = datetime.datetime.today().date()
		# time = datetime.datetime.today().time()
		# print("date ==> ", date)
		# print("time ==> ", time)

		# return render(request, self.template_name, {"date":date, "time":time, 'user': user, 'answers':answers})

		try:
			superuser = request.user		
			print("User ==> ", superuser)

			if superuser.is_authenticated & superuser.is_superuser:
				print("Authenticated username => ", superuser.username)
				users = Profile.objects.all()

				return render(request, self.template_name, {"Status":"Success", "superuser":superuser ,'users':users})
				
			else:
				print("Anonymous user")
				return render(request, self.template_name, {})
		except Exception as e:
			raise e

		return render(request, self.template_name,{})


	def post(self, request, *args, **kwargs):
		firstname = request.POST.get('fname')
		print("Name: ",firstname)
		email =request.POST.get('email')
		print("email: ",email)
		age = request.POST.get('age')
		print("age: ",age)
		country =request.POST.get('country')
		print("country: ",country)
		gender = request.POST.get('gender')
		print("gender: ",gender)
		phone = request.POST.get('phone')
		print("phone: ",phone)
		choose = request.POST.get('choose')
		print("choose: ",choose)

		concent = request.POST.get('concent')
		print("concent: ",concent)
		sms_concent = False

		# if concent == "on":
		# 	sms_concent = True
		# 	response = requests.post("https://api.ontraport.com/1/Contacts",data={'firstname':firstname,'email':email , 'sms_number':phone, 'bulk_sms':1 }, headers={'Accept': 'application/json','Api-Appid': '2_152916_N6PZnweLG', 'Api-Key': 'uwdB4h6whxTCffq'})
		# 	json_response = response.json()
		# 	print("json_response user id === ",json_response['data']['id'])
		# else:	
		# 	response = requests.post("https://api.ontraport.com/1/Contacts",data={'firstname':firstname,'email':email , 'sms_number':phone, 'bulk_sms':0 }, headers={'Accept': 'application/json','Api-Appid': '2_152916_N6PZnweLG', 'Api-Key': 'uwdB4h6whxTCffq'})
		# 	json_response = response.json()
		# 	print("json_response user id === ",json_response['data']['id'])

		user = Profile(firstname=firstname, email=email, age=age, country=country, gender=gender, phone=phone, problem=choose, sms_concent=sms_concent)
		user.save()		

		return HttpResponseRedirect('quiz/')


#Start Quiz/Survey
class QuestionView(View):	
	 
	def get(self, request, *args, **kwargs):
		user = Profile.objects.latest('id')
		print("user===> ", user )
				
		if 	Answer.objects.filter(user=user.id).exists():
			ans = Answer.objects.filter(user=user.id)

			count = len(ans)
		else:
			count=0
		
		if count<200: #200
			questions = Question.objects.get(id=count+1)
			return JsonResponse({"status":"Success","questions": questions.question, "user":user.firstname, "attempted": count})			
		else:			
			questions = Question.objects.get(id=1)
			return JsonResponse({"status":"Success","questions": questions.question, "user":user.firstname, "attempted": count})
			

		return JsonResponse({"status":"failed", "user":user.firstname, "attempted": count})
		

#To load next unanswered question
def loadNextQuestion(request, id, value):
	ques = Question.objects.all()
	user = Profile.objects.latest('id')

	if 	Answer.objects.filter(user=user.id).exists():
		ans = Answer.objects.filter(user=user.id)
		count = len(ans)
	else:
		count=0

	ques = Question.objects.get(id=int(id))
	if Answer.objects.filter(question = ques, user=user.id).exists():
		Answer.objects.filter(question = ques, user=user.id).update(answer=value)
	else:
		ans = Answer(question=ques, user=user, answer=value)
		ans.save()	
	
	quesID = int(id)+1
	# print("Next question ID---> ",quesID)

	if quesID<=200 or quesID<=count: #200
		# print("survey not cocmpleted")

		if quesID<=count:
			ques = Question.objects.get(id=quesID)
			ans = Answer.objects.filter(question=ques.id, user=user.id).values("answer")
			return JsonResponse({"status":"Success", "questions": ques.question, "answer":ans[0]["answer"], "attempted": count})
		else:
			questions = Question.objects.get(id=quesID)		
			return JsonResponse({"status":"Success", "questions": ques.question, "answer":"none", "attempted": count})
	else:
		# print("End Survey/ show result")
		result = Answer.objects.filter(user=user.id).values("user")
		print("Result===> ", result[0]['user'])
		user_profile = Profile.objects.get(id=result[0]['user'])

		#Update Message plain text according to user name
		plainMsgText = "Hey "+user_profile.firstname+", congratulations for completing the survey of 200 questions!"

		# response = requests.put("https://api.ontraport.com/1/message", data={'id':363, 'plaintext':plainMsgText},
  #   headers={'Accept': 'application/json','Api-Appid': '2_152916_N6PZnweLG', 'Api-Key': 'uwdB4h6whxTCffq'})
		# json_response = response.json()


		#Added tag to contact

		# if user_profile.problem == 'stress':
		# 	print("stress")
		# 	response = requests.put("https://api.ontraport.com/1/objects/tag", data={'objectID':0, 'add_list':75,'ids':user_profile.ontra_contact_id},
  #   headers={'Accept': 'application/json','Api-Appid': '2_152916_N6PZnweLG', 'Api-Key': 'uwdB4h6whxTCffq'})
		# 	json_response = response.json()

		# if user_profile.problem == 'health' or user_profile.problem == '1d': #1d
		# 	print("health/1d")
		# 	response = requests.put("https://api.ontraport.com/1/objects/tag", data={'objectID':0, 'add_list':76,'ids':user_profile.ontra_contact_id},
  #   headers={'Accept': 'application/json','Api-Appid': '2_152916_N6PZnweLG', 'Api-Key': 'uwdB4h6whxTCffq'})
		# 	json_response = response.json()

		# if user_profile.problem == 'career':
		# 	print("career")
		# 	response = requests.put("https://api.ontraport.com/1/objects/tag", data={'objectID':0, 'add_list':77,'ids':user_profile.ontra_contact_id},
  #   headers={'Accept': 'application/json','Api-Appid': '2_152916_N6PZnweLG', 'Api-Key': 'uwdB4h6whxTCffq'})
		# 	json_response = response.json()

		# if user_profile.problem == 'relationships' or user_profile.problem == '2d': #2d
		# 	print("relationships/2d")
		# 	response = requests.put("https://api.ontraport.com/1/objects/tag", data={'objectID':0, 'add_list':78,'ids':user_profile.ontra_contact_id},
  #   headers={'Accept': 'application/json','Api-Appid': '2_152916_N6PZnweLG', 'Api-Key': 'uwdB4h6whxTCffq'})
		# 	json_response = response.json()

		# if user_profile.problem == 'money' or user_profile.problem == '3d': #3d
		# 	print("money/3d")
		# 	response = requests.put("https://api.ontraport.com/1/objects/tag", data={'objectID':0, 'add_list':79,'ids':user_profile.ontra_contact_id},
  #   headers={'Accept': 'application/json','Api-Appid': '2_152916_N6PZnweLG', 'Api-Key': 'uwdB4h6whxTCffq'})
		# 	json_response = response.json()

		# response = requests.put("https://api.ontraport.com/1/objects/tag", data={'objectID':0, 'add_list':77,'ids':user_profile.ontra_contact_id},
  #   headers={'Accept': 'application/json','Api-Appid': '2_152916_N6PZnweLG', 'Api-Key': 'uwdB4h6whxTCffq'})

		# response = requests.put("https://api.ontraport.com/1/Contacts", data={'id':user_profile.ontra_contact_id, 'title':"survey completed"},
  #   headers={'Accept': 'application/json','Api-Appid': '2_152916_N6PZnweLG', 'Api-Key': 'uwdB4h6whxTCffq'})
		# json_response = response.json()
		print("-------------- Generate Result ----------------")

		return JsonResponse({"status":"failed", "questions": ques.question, "attempted": count, 'user_id':user.id})		

	return render(request, "scientogy.html")


#To load next already answered question
def nextQuestion(request, id):
	user = Profile.objects.latest('id')

	count = 0
	if 	Answer.objects.filter(user=user.id).exists():
		ans = Answer.objects.filter(user=user.id)
		count = len(ans)
	else:
		count=0

	quesID = int(id)+1

	if quesID<=count+1:
		ques = Question.objects.get(id=quesID)
		if quesID<=count:
			ans = Answer.objects.filter(question=ques.id, user=user.id).values("answer")
			return JsonResponse({"status":"Success", "questions": ques.question, "answer":ans[0]["answer"]})
		else:
			ques = Question.objects.get(id=quesID)
			return JsonResponse({"status":"Success", "questions": ques.question, "answer":'none'})			
	else:
		# print("Current Question")		
		return JsonResponse({"status":"failed"})

	return HttpResponseRedirect('/quiz')


#To load previous question
def previousQuestion(request, id):
	user = Profile.objects.latest('id')
	
	if 	Answer.objects.filter(user=user.id).exists():
		ans = Answer.objects.filter(user=user.id)
		count = len(ans)
	else:
		count=0

	quesID = int(id)-1
	if quesID>0:
		ques = Question.objects.get(id=quesID)
		ans = Answer.objects.filter(question=ques.id, user=user.id).values("answer")
		# print("Answer",ans[0]["answer"])
		return JsonResponse({"status":"Success", "questions": ques.question, "answer":ans[0]["answer"]})		
	else:
		# print("First Question")
		try:
			ques = Question.objects.get(id=1)
			ans = Answer.objects.filter(question=ques.id, user=user.id).values("answer")
			return render(request, "scientogy.html", {"questions": ques.question, "answer":ans[0]["answer"]})
		except DoesNotExist:
			return HttpResponseRedirect('/quiz')

	return HttpResponseRedirect('/quiz')

# Survey Compeletion View
class CompletionView(TemplateView):
	template_name = "completion.html" #"survey.html"
	model = Profile


	def get(self, request, *args, **kwargs):
		status = ""
		if self.kwargs['value']:
			print("self.kwargs['value'] ==> ", self.kwargs['value'])
			status = self.kwargs['value']		

		user = Profile.objects.latest('id')
	
		nextday = date.today() + datetime.timedelta(days=1)
		nextDate = nextday.strftime("%B %d, %Y")

		return render(request, self.template_name, {"user":user.firstname, "current_date":nextDate, "status":status})



def searchByUser(request):	
	q = request.GET.get('q')
	print("q ==> ",q)
	category = request.GET.get("categories")
	print("category ==> ",category)
	if category=="all":
		if q:
			records = LocationData.objects.filter(location__location__contains=q)
		else:
			records = LocationData.objects.all()
	else:
		if q:
			records = LocationData.objects.filter(location__location__contains=q, categories__slug__contains=category)
		else:
			records = LocationData.objects.filter(categories__slug__contains=category)
	categories = Categories.objects.all() 
	print("categories ==> ",categories)
	return render(request, "database.html" , {'records':records,'categories':categories,"cat_search_item":category,"search_item":q})

class PrivacyView(TemplateView):
	template_name = "privacy.html"

	def get(self, request, *args, **kwargs):

		return render(request, self.template_name, {})

class CookieView(TemplateView):
	template_name = "cookie.html"
	
	def get(self, request, *args, **kwargs):

		return render(request, self.template_name, {})

class LeagalView(TemplateView):
	template_name = "leagal.html"
	
	def get(self, request, *args, **kwargs):

		return render(request, self.template_name, {})

class TermsView(TemplateView):
	template_name = "terms.html"
	
	def get(self, request, *args, **kwargs):

		return render(request, self.template_name, {})

##To Scrap questions from given html files and save in question model.
# def addQuestions(request):
# 	filepath = "/home/aviox/work/Question_Pro/oca2.html"
# 	count=1
# 	with open(filepath, encoding="utf8") as f:
# 		contents = f.read()
# 		soup = BeautifulSoup(contents, "html.parser")
# 		table = soup.find("table", {"border":"1"})
# 		tr_tags = table.findAll("tr", {"bgcolor":"#D7E0E3"})
# 		if count==1:
# 			for tr in tr_tags:
# 				td_tags = tr.findAll("td")
# 				print("Question_no: ",td_tags[0].text)
# 				print("Question: ",td_tags[1].text)
# 				ques = Question(question=td_tags[1].text)
# 				ques.save()
# 				print("Question Saved")
# 			count +=1
# 	return HttpResponseRedirect('/quiz')

