
from django.core.mail import EmailMessage
from django.core.mail import send_mail , BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect ,JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from mainapp.models import *
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from .utils import Calendar
from .forms import EventForm
# Create your views here.
import facebook
from pyfacebook import GraphAPI
from .models import *
import datetime
from datetime import datetime, timedelta
from time import time, ctime

id = "1316976275431455"
secret = "1a41639c59596b4b462dac98a4f55f20"
redirect_uri = 'http://localhost:8000/fblogin/'
scope = ['pages_read_engagement', 'read_insights', 'public_profile']
# scope = ['email','public_profile','pages_show_list']
# Create your views here.
api = GraphAPI(app_id=id, app_secret=secret, application_only_auth=True)
graph = facebook.GraphAPI()

def home(request):
    yesterday = datetime.now() - timedelta(2)
    print(yesterday) # Get timezone naive no
    seconds = yesterday.timestamp()
    a = int(seconds)
    print(a)
    return render(request, 'main.html')

def userlist(request):
    
    usertype = UserType.objects.all()
    context = {'usertype' : usertype}
    return render(request, 'dashboard/user.html', context)
def analyatics(request):
    return render(request, 'dashboard/analyatics.html')
def  signup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        checkemail = User.objects.filter(email=email)
        checkuser = User.objects.filter(username=username)
        
        if len(checkemail)>0:
            messages.error(request, "Email is already exits.")
            return render(request, 'signup.html')
        if len(checkuser)>0:
            messages.error(request, "User Name is already exits.")
            return render(request, 'signup.html')
    
        if len(username) > 10:
            messages.error(request, " Your user name must be under 10 characters")
            return render(request, 'signup.html')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return render(request, 'signup.html')
        if password != cpassword:
            messages.error(request, " Passwords do not match")
            return render(request, 'signup.html')

        # Create the user
        user = User.objects.create_user(username, email, password)
        print(user)
        user_type = request.POST['user_type']
        userType = UserType(user_type = user_type , user=user)
        userType.save()
        user.save()
        
        messages.success(request, "You have succesfully Registerd.")
        return render(request, 'signup.html')
    return render(request, 'signup.html')

def signin(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['uname']
        password = request.POST['password']
        user = authenticate(username=username, password=password)  
        if user is not None:
            accounttype = UserType.objects.get(user=user)
            type = accounttype.user_type
            login(request  , user)
            if(type=="Admin"):
                request.session['Utype']=type
                return redirect('/analyatics/')
            if(type=="Employee"):
                request.session['Utype']=type
                return redirect('/analyatics/')
                #return render(request, 'user/home.html')
            if(type=="User"):
                request.session['Utype']=type
                return redirect('/analyatics/')
                #return render(request, 'company/dashboard.html')

        else:
            messages.error(request, "Invalid credentials! Please try again")
            return render(request, "login.html")
    return render(request, 'login.html')
    
def strategy(request):
    if request.method == "POST":
       note1 = request.POST['note']
       user1 = request.user
       date1 = datetime.now()
       context = startegy1( user= user1 ,    comment = note1 , date = date1)
       context.save()
       messages.success(request, "Your content succesfully Added.")
       return redirect('/showstrategy')
    return render(request, 'dashboard/strategy.html')
def showstrategy(request):
    strategy = startegy1.objects.all()
    context = {'strategy':strategy}
    return render(request, 'dashboard/showstragy.html' , context)

def updatestrategy(request , id):
   updatestrategy = startegy1.objects.get(pk=id)
   context = {'updatestrategy': updatestrategy}
   if request.method == "POST":
       note1 = request.POST['note']
       user1 = request.user
       date1 = datetime.now()
       updatestrategy  =  startegy1.objects.get(pk=id)
       updatestrategy.comment = note1
       updatestrategy.date = date1
       updatestrategy.user = user1
       updatestrategy.save()
       messages.success(request, "Your content is successfully updated.")
       return redirect('/showstrategy')
   return render(request, 'dashboard/strategy.html' ,context)
def deletestrategy(request,id):
    delete = startegy1.objects.get(pk=id)
    delete.delete()
    messages.success(request, "Your content is successfully deleted.")
    return redirect('/showstrategy')
def logo(request):
    if request.method == "POST":
       file = request.FILES['file1']
       context = addlogo(logo = file)
       context.save()
       messages.success(request, "Your content is successfully Added.")
       return redirect('/showlogo')
    return render(request, 'dashboard/logo.html')
def competitors(request):
    return render(request, 'dashboard/competitors.html')

def billing(request):
    if request.method == "POST":
       file = request.FILES['file1']
       context = billingtable(  invoice  = file)
       context.save()
       messages.success(request, "Your content is successfully Added.")
       return redirect('/showbill')
    return render(request, 'dashboard/billing.html')
def showbill(request):
   
     showinvoice =  billingtable.objects.all()
     context = {'showinvoice':  showinvoice}
     return render(request, 'dashboard/showbill.html', context)

def updatebill(request , id):
   updatelogo = billingtable.objects.get(pk=id)
   context = {'updatelogo': updatelogo}
   if request.method == "POST":
       file1 = request.FILES['file1']
       updatebill = billingtable.objects.get(pk=id)
       updatebill.invoice = file1
       updatebill.save()
       messages.success(request, "Your content is successfully updated.")
       return redirect('/showbill')
   return render(request, 'dashboard/billing.html' ,context)

def deletebill(request,id):
    delete = billingtable.objects.get(pk=id)
    delete.delete()
    messages.success(request, "Your content is successfully deleted.")
    return redirect('/showbill')
def socialmedia(request):
    return render(request, 'dashboard/socialmedia.html')

def calender(request):
    return render(request, 'dashboard/calender.html')

def ApproveContent(request):
    if request.method == "POST":
       note1 = request.POST['tag']
       file = request.FILES['file1']
       context = content(  video = file , tag = note1)
       context.save()
       messages.success(request, "Your content is successfully Added.")
       return redirect('/showcontent')
       
    return render(request, 'dashboard/Approvecontent.html')

def showcontent(request):
   
     showcontent1= content.objects.all()
     context = {'content': showcontent1}
     return render(request, 'dashboard/showcontent.html', context)
def updatecontent(request , id):
   content1 = content.objects.get(pk=id)
   context = {'content': content1}
   if request.method == "POST":
       note1 = request.POST['tag']
       file = request.FILES['file1']
       updatecontent = content.objects.get(pk=id)
       updatecontent.tag = note1
       updatecontent.video = file
       updatecontent.save()
       messages.success(request, "Your content is successfully updated.")
       return redirect('/showcontent')
   return render(request, 'dashboard/Approvecontent.html' ,context)
def deletecontent(request,id):
    delete1 = content.objects.get(pk=id)
    delete1.delete()
    messages.success(request, "Your content is successfully Deleted.")
    return redirect('/showcontent')
def calenderview(request):
    return render(request, 'dashboard/calenderview.html')
def starttoday(request):
    if request.method == 'POST':
        fname = request.POST ['field1']
        lname = request.POST ['field2']
        dealership = request.POST ['field3']
        email = request.POST['field4']
        phoneno = request.POST ['field5']
        message1 = request.POST ['field6']
        subject = request.POST ['field9']
        starttoday = SchduleDemo(firstname= fname , lastname = lname ,  DealershipName = dealership , Emailaddress = email , PhoneNo = phoneno ,    help =  message1  ,  Question = subject  )
        starttoday.save()
        #SEND AN EMAI
        
        mail_subject = subject
        message2 = 'Sender Name:......' +  fname  + '\n' + 'Sender EmailAdress:.........' +  email + '\n'+ 'Sender Phone:......' + phoneno + '\n'+  'Sender Dealership Name:.......' + dealership  + '\n' +  'Sender Subject:.......' +  subject + '\n' + 'Sender Question:.......' +  message1
        f_email = email
        send_mail(
              mail_subject,  message2, f_email , ['sales@thekpadvantage.com']

        )
        SuccessMessage  =  "A member of our team will contact you soon" 
        context = {'sucessMessage' : SuccessMessage}
        return render(request, 'starttoday.html' ,context)

    else:
        return render(request, 'starttoday.html')
def showstarttoday(request):
         show = SchduleDemo.objects.all()
         context = {'show': show}
         return render(request, 'dashboard/showstarttoday.html' , context)
def updateschdule(request , id):
          show = SchduleDemo.objects.get(pk=id)
          context = {'show': show}
          if request.method == "POST":
                  fname = request.POST ['fname']
                  lname = request.POST ['lname']
                  dealership = request.POST ['dealership']
                  email = request.POST['email']
                  phoneno = request.POST ['phone']
                  message1 = request.POST ['help']
                  subject = request.POST ['question']
                  updateschdule = SchduleDemo.objects.get(pk=id)
                  updateschdule.firstname = fname
                  updateschdule.lastname = lname
                  updateschdule.DealershipName = dealership
                  updateschdule.Emailaddress = email
                  updateschdule.PhoneNo = phoneno
                  updateschdule.help = message1
                  updateschdule.Question = subject
                  updateschdule.save()
                  messages.success(request, "Your content is successfully updated.")
                  return redirect('/showstarttoday')

          return render(request, 'dashboard/updateschdule.html' ,context)

def schduledelete(request,id):
    employee = SchduleDemo.objects.get(pk=id)
    employee.delete()
    messages.success(request, "Your content is successfully Deleted.")
    return redirect('/showstarttoday')

def contactus(request):
    if request.method == 'POST':
        fname = request.POST ['field1']
        lname = request.POST ['field2']
        dealership = request.POST ['field3']
        email = request.POST['field4']
        phoneno = request.POST ['field5']
        message1 = request.POST ['field6']
        subject = request.POST ['field9']
        starttoday = SchduleDemo(firstname= fname , lastname = lname ,  DealershipName = dealership , Emailaddress = email , PhoneNo = phoneno ,    help =  message1  ,  Question = subject  )
        starttoday.save()

        #SEND AN EMAIL
        mail_subject = subject
        message2 = 'Sender Name:......' +  fname  + '\n' + 'Sender EmailAdress:.........' +  email + '\n'+ 'Sender Phone:......' + phoneno + '\n'+  'Sender Dealership Name:.......' + dealership  + '\n' +  'Sender Subject:.......' +  subject + '\n' + 'Sender Question:.......' +  message1
        f_email = email
        send_mail(
              mail_subject,  message2, f_email , ['sales@thekpadvantage.com']

        )
        SuccessMessage  =  "A member of our team will contact you soon" 
        context = {'sucessMessage' : SuccessMessage}
        return render(request, 'contactus.html' ,context)

    else:
        return render(request, 'contactus.html')

def ulogout(request):
    logout(request)
    try:
        del request.session['Utype']
    except KeyError:
        pass
    return redirect('/')

def usertdelete(request,id):
    employee = User.objects.get(pk=id)
    employee.delete()
    messages.success(request, "Your content is successfully Deleted.")
    return redirect('/user')

def UpdateUser(request, id):
     
   usertype = UserType.objects.get(pk=id)
   context = {'usertype': usertype}
   if request.method == "POST":
       name = request.POST['username']
       user_type = request.POST['ut']
       email = request.POST['email']
       checkemail = User.objects.filter(email=email)
       checkuser = User.objects.filter(username=name)
       usertype1 = UserType.objects.get(pk=id)
       userid = usertype1.user.id
       user = User.objects.get(id = userid)
       usertype1.user_type = user_type
       user.username = name 
       user.email = email
       usertype1.save()
       user.save()
       messages.success(request, "Your content is successfully updated.")
       return redirect('/user')
   return render(request, 'dashboard/userform.html', context)


def showlogo(request):
   
     showlogo = addlogo.objects.all()
     context = {'showlogo': showlogo}
     return render(request, 'dashboard/showlogo.html', context)

def updatelogo(request , id):
   updatelogo = addlogo.objects.get(pk=id)
   context = {'updatelogo': updatelogo}
   if request.method == "POST":
       logo1 = request.FILES['file1']
       updatelogo  = addlogo.objects.get(pk=id)
       updatelogo.logo = logo1
       updatelogo.save()
       messages.success(request, "Your content is successfully updated.")
       return redirect('/showlogo')
   return render(request, 'dashboard/logo.html' ,context)

def deletelogo(request,id):
    delete = addlogo.objects.get(pk=id)
    delete.delete()
    messages.success(request, "Your content is successfully deleted.")
    return redirect('/showlogo')

def calender(request):
    return render(request, 'dashboard/calendar.html')
class CalendarView(generic.ListView):
    model = Event
    template_name = 'dashboard/calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        
    return render(request, 'dashboard/event.html', {'form': form})


    
def fblogin(request):   
    if request.GET.get('code'):
        code = request.GET.get('code')
        x = graph.get_access_token_from_code(
            code=code, redirect_uri=redirect_uri, app_id=id, app_secret=secret)
        at = x['access_token']
        user_info = graph.request(path='me?', args={'access_token': at})        
        user = fb_users.objects.create(
            user_id=user_info['id'], user_name=user_info['name'], user_access_token=at)
        user.save()
        page_data = api.exchange_long_lived_page_access_token(
            user_id=user_info['id'], access_token=at)
        for i in page_data['data']:           
            page = fb_user_pages.objects.create(
                page_id=i['id'], page_name=i['name'], page_access_token=i['access_token'])
            page.save()
            user.pages.add(page)

        return redirect('/analyatics/#')
    else:
        return redirect('/analyatics/#')


def fb_page_data(request, id, days, data):
    s = fb_user_pages.objects.get(page_id=id)
    until = (datetime.now()).timestamp()
    since = (datetime.now() - timedelta(days+1)).timestamp()

    if s:
        if api.debug_token(input_token=s.page_access_token)['data']['is_valid']:
            values = []
            labels = []
            if data == 'engagement':
                engagement = graph.request(
                    path=f'{s.page_id}/insights?metric=page_post_engagements&period=day&since={int(since)}&until={int(until)}',
                    args={'access_token': s.page_access_token})
                for v in engagement['data'][0]['values']:
                    values.append(v['value'])
                    labels.append(v['end_time'][:-14])
            if data == 'views':
                engagement = graph.request(
                    path=f'{s.page_id}/insights?metric=page_views_total&period=day&since={int(since)}&until={int(until)}',
                    args={'access_token': s.page_access_token})
                for v in engagement['data'][0]['values']:
                    values.append(v['value'])
                    labels.append(v['end_time'][:-14])
            if data == 'likes':
                engagement = graph.request(
                    path=f'{s.page_id}/insights?metric=page_fans&period=day&since={int(since)}&until={int(until)}',
                    args={'access_token': s.page_access_token})
                for v in engagement['data'][0]['values']:
                    values.append(v['value'])
                    labels.append(v['end_time'][:-14])
            if data == 'clicks':
                engagement = graph.request(
                    path=f'{s.page_id}/insights?metric=page_total_actions&period=day&since={int(since)}&until={int(until)}',
                    args={'access_token': s.page_access_token})
                for v in engagement['data'][0]['values']:
                    values.append(v['value'])
                    labels.append(v['end_time'][:-14])

            if data == 'impressions':
                engagement = graph.request(
                    path=f'{s.page_id}/insights?metric=page_impressions&period=day&since={int(since)}&until={int(until)}',
                    args={'access_token': s.page_access_token})
                for v in engagement['data'][0]['values']:
                    values.append(v['value'])
                    labels.append(v['end_time'][:-14])
            if data == 'reactions':
                engagement = graph.request(
                    path=f'{s.page_id}/insights?metric=page_actions_post_reactions_like_total&period=day&since={int(since)}&until={int(until)}',
                    args={'access_token': s.page_access_token})
                for v in engagement['data'][0]['values']:
                    values.append(v['value'])
                    labels.append(v['end_time'][:-14])

            values.append(max(values)*1.5)
            return JsonResponse({'values': values, 'labels': labels})
        else:
            return redirect('analyatics')

    else:
        s.delete()
        return redirect('analyatics')


def fb_page_data1(request, id, days):
    s = fb_user_pages.objects.get(page_id=id)
    t = 0
    period = 'day'
    if days == 1:
        t = 1
    until = (datetime.now() - timedelta(t)).timestamp()
    since = (datetime.now() - timedelta(t+1)).timestamp()
    if days == 7:
        period = 'week'
    if days == 28:
        period = 'days_28'
    if s:
        if api.debug_token(input_token=s.page_access_token)['data']['is_valid']:            
            context = {}
            data = graph.request(
                path=f'{s.page_id}/insights?metric=page_post_engagements,page_views_total,page_fans,page_total_actions,page_impressions,page_actions_post_reactions_like_total&period={period}&since={int(since)}&until={int(until)}',
                args={'access_token': s.page_access_token})
            if days == 7 or days == 28:
                page_fans = graph.request(
                    path=f'{s.page_id}/insights?metric=page_fans&period=day&since={int(since)}&until={int(until)}',
                    args={'access_token': s.page_access_token})               
                context[page_fans['data'][0]['name']]=page_fans['data'][0]['values'][0]['value']            
            for d in data['data']:                
                context[d['name']] = d['values'][0]['value']
            return JsonResponse(context)
        else:
            return redirect('analyatics')

    else:
        s.delete()
        return redirect('analyatics')


def facebook_page(request, slug):
    s = fb_user_pages.objects.filter(slug=slug)    
    context = {'id': s[0].page_id}
    if s:
        if api.debug_token(input_token=s[0].page_access_token)['data']['is_valid']:
            data = graph.request(
                path=f'{s[0].page_id}/insights?metric=page_post_engagements,page_views_total,page_fans,page_total_actions,page_impressions,page_actions_post_reactions_like_total&period=day',
                args={'access_token': s[0].page_access_token})            
            for d in data['data']:              
                context[d['name']] = d['values'][0]['value']            
        else:
            return redirect('analyatics')

    else:
        s.delete()
        return redirect('analyatics')
    return render(request, 'dashboard/fbanalyatics.html', context)


def analyatics(request):
    print(time())
    url = ''
    fb_user = fb_users.objects.all()
    if fb_user:
        if not api.debug_token(input_token=fb_user[0].user_access_token)['data']['is_valid']:
            url = api.get_authorization_url(
                redirect_uri=redirect_uri, scope=scope)[0]
        else:
            fb_user = fb_user[0]
    else:
        url = api.get_authorization_url(
            redirect_uri=redirect_uri, scope=scope)[0]

    context = {
        'fbloginurl': url,
        'user_data': fb_user
    }
    # print(fb_user.user_access_token)
    # print(api.debug_token(input_token=fb_user.user_access_token)['data']['is_valid'])
    # at = 'EAAStyG8TIB8BAND099m6fxC3soHH2hfv90kBPOYwGqVoU7dy0CrQy4yaYF3hpj9BkdFnZBqOQkTjKw59ftPu24ZCZBmASiwap5bUaqSZCzCBE2VUofgUZC1iwjIjOcxnIb3pSCsc5h19aFBZBWDd8dgMf1IhtPSCZCEPuwn8d1Taq7MRZAatjulTvlKf2fc1ak4YTaA9AH9C2tD62ZBqkCPEGa8TBGZCCsxEjxXZBiAtZCMwUTZClciL0aI62'
    # user_info = graph.request(path='me?', args={'access_token': at})
    # # token = fbapi_token.objects.create(access_token=at)
    # # token.save()

    # print(page_data['data'])
    # db = api.debug_token(input_token='EAAStyG8TIB8BAAqkGJjZCoqDSzWaHBQgZB0XXjduJndR3b3xomlneYjw5RXdAknuuXMlo6NKlttxZC5r0AtZBWBPgFUaCgSP837iCgfo7I1ia0lQVeYSZBLY4cA4l1waD8KRI3z23CK5e34tXIKvteER5QwsyISV9REWCjmgAWh9rGh8CsOug18kpIdZCZBFXZCSdjRzKhPdXrUuUb7aKNL6f2WtrhGEPbDVQsmEUEMBzq84pL3X6ZAA5')
    # # db1 = graph.debug_access_token(token='EAAStyG8TIB8BAAqkGJjZCoqDSzWaHBQgZB0XXjduJndR3b3xomlneYjw5RXdAknuuXMlo6NKlttxZC5r0AtZBWBPgFUaCgSP837iCgfo7I1ia0lQVeYSZBLY4cA4l1waD8KRI3z23CK5e34tXIKvteER5QwsyISV9REWCjmgAWh9rGh8CsOug18kpIdZCZBFXZCSdjRzKhPdXrUuUb7aKNL6f2WtrhGEPbDVQsmEUEMBzq84pL3X6ZAA5',app_id=id,app_secret=secret)
    # print(db['data']['is_valid'])
    # print(db1)
    # lgt = api.exchange_long_lived_page_access_token(access_token=token)
    # print(lgt)
    # user_info = api.get(path='me?',args={'access_token': token})
    # print(user_info)
    if api:

        return render(request, 'dashboard/analyatics.html', context)
    else:
        return render(request, 'dashboard/analyatics.html', context)