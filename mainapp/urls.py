from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('analyatics/', views.analyatics, name='analyatics'),
      path('signin/', views.signin, name='signin'),
        path('schdule/', views.signup, name='signup'),
          path('strategy/', views.strategy, name='strategy'),
           path('logo/', views.logo, name='logo'),
           path('competitors/', views.competitors, name='competitors'),
                path('billing/', views.billing, name='billing'),
                  path('socialmedia/', views.socialmedia, name='socialmedia'),
                      path('calender/', views.calender, name='calender'),
                                  path('Approvecontent/', views.ApproveContent, name='Approvecontent'),
                                    path('calenderview/', views.calenderview, name='calenderview'),
                                        path('contactus/', views.contactus, name='contactus'),
                                         path('starttoday/', views.starttoday, name='starttoday'),

]