# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from main.models import teacher, users
from django.http import HttpResponse
from django import template
import pandas as pd
import openpyxl
import re
import os
from django.db.models import Q
from django.conf import settings

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    if "GET" == request.method:
        context = {}
        teachers = ''
        context['segment'] = 'tables'
        if 'search' in request.GET:
            search_term = request.GET['search']
            if(search_term):
                context['teachers'] = teacher.objects.filter(Q(subjects_taught__contains=search_term)|
                Q(last_name__startswith=search_term))
            else:
                context['teachers'] = teacher.objects.filter()
            #articles = teacher.objects.all().filter(feeder__icontains=search_term) 
        else:
            context['teachers'] = teacher.objects.filter()

        html_template = loader.get_template( 'tables.html' )
        return HttpResponse(html_template.render(context, request))
    else:
        context = {}
        teachers = ''
        context['segment'] = 'tables'
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(os.path.join(settings.BASE_DIR, 'main', 'static', 'assets', 'files', str(excel_file)))
        worksheet = wb["Teachers"]
        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows(min_row=2):
            row_data = dict()
            subjects_list = list()
            subjects = row[6].value
            if(row[3].value):
                email_validate = EMAIL_REGEX.match(row[3].value)
            else:
                email_validate = False
            if(subjects):
                subjects_list = [x.strip() for x in subjects.split(',')]
            if(str(row[2].value)):
                fileName, fileExtension = os.path.splitext(str(row[2].value))
                if(fileExtension):
                    profile_picture = str(row[2].value)
                else:
                    profile_picture = ''
            
            if(len(subjects_list) <= 5 and email_validate):
                row_data["first_name"] = str(row[0].value)
                row_data["last_name"] = str(row[1].value)
                row_data["profile_picture"] = profile_picture
                row_data["email"] = str(row[3].value)
                row_data["phone"] = ''.join(x for x in str(row[4].value) if x.isdecimal())
                row_data["room_no"] = str(row[5].value)
                row_data["subjects_taught"] = str(row[6].value)
                    
            if(len(row_data) > 0):
                excel_data.append(row_data)
            #print(excel_data)
            try:
                batch = [teacher(first_name=row['first_name'], last_name=row['last_name'],
                profile_picture=row['profile_picture'], email=row['email'],  phone=row['phone'],  room_no=row['room_no'],
                subjects_taught=row['subjects_taught'] ) for row in excel_data]
                teacher.objects.bulk_create(batch)

                context['teachers'] = teacher.objects.filter()
                html_template = loader.get_template( 'tables.html' )
                return HttpResponse(html_template.render(context, request))
            except:
            
                html_template = loader.get_template( 'page-500.html' )
                return HttpResponse(html_template.render(context, request))

        

def profile(request, id):
    context = {}
    teachers = ''
    context['segment'] = 'profile'
    context['teachers'] = teacher.objects.filter(id=id)[0]
    html_template = loader.get_template( 'profile.html' )
    return HttpResponse(html_template.render(context, request))

def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        context['teachers'] = teacher.objects.filter()
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))



def imports(request):
    df = pd.read_excel('file_name_here.xlsx', sheet_name='Sheet1')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response
