
from django.core.mail import EmailMessage
from django.core.mail import send_mail , BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request, 'main.html')
def analyatics(request):
    return render(request, 'dashboard/analyatics.html')
def  signup(request):
    if request.method == 'POST':
        fname = request.POST ['field1']
        lname = request.POST ['field2']
        dealership = request.POST ['field3']
        email = request.POST['field4']
        phoneno = request.POST ['field5']
     

        #SEND AN EMAIL
        mail_subject = email
        message2 = 'Sender Name:......' +  fname  + '\n' + 'Sender EmailAdress:.........' +  email + '\n'+ 'Sender Phone:......' + phoneno + '\n'+  'Sender Dealership Name:.......' + dealership  
        f_email = email
        send_mail(
              mail_subject,  message2, f_email , ['ahsanaziz895@gmail.com']

        )
        SuccessMessage  =  "your message is send to team , Team will contact you soon" 
        context = {'sucessMessage' : SuccessMessage}
        return render(request, 'signup.html' ,context)

    else:
        return render(request, 'signup.html')
def signin(request):
    return render(request, 'login.html')
    
def strategy(request):
    return render(request, 'dashboard/strategy.html')

def logo(request):
    return render(request, 'dashboard/logo.html')
def competitors(request):
    return render(request, 'dashboard/competitors.html')

def billing(request):
    return render(request, 'dashboard/billing.html')

def socialmedia(request):
    return render(request, 'dashboard/socialmedia.html')

def calender(request):
    return render(request, 'dashboard/calender.html')

def ApproveContent(request):
    return render(request, 'dashboard/Approvecontent.html')
def calenderview(request):
    return render(request, 'dashboard/calenderview.html')

def contactus(request):
    if request.method == 'POST':
        fname = request.POST ['field1']
        lname = request.POST ['field2']
        dealership = request.POST ['field3']
        email = request.POST['field4']
        phoneno = request.POST ['field5']
        message1 = request.POST ['field6']
        subject = request.POST ['field9']

        #SEND AN EMAIL
        mail_subject = subject
        message2 = 'Sender Name:......' +  fname  + '\n' + 'Sender EmailAdress:.........' +  email + '\n'+ 'Sender Phone:......' + phoneno + '\n'+  'Sender Dealership Name:.......' + dealership  + '\n' +  'Sender Subject:.......' +  subject + '\n' + 'Sender Question:.......' +  message1
        f_email = email
        send_mail(
              mail_subject,  message2, f_email , ['ahsanaziz895@gmail.com']

        )
        SuccessMessage  =  "your message is send to team , Team will contact you soon" 
        context = {'sucessMessage' : SuccessMessage}
        return render(request, 'contactus.html' ,context)

    else:
        return render(request, 'contactus.html')