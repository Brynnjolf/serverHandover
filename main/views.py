from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404
from django.forms.models import model_to_dict
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from subprocess import Popen, PIPE, STDOUT
import json
import ast
from .models import *
from django.views.decorators.csrf import csrf_exempt
import saving_data
import re

# Create your views here.

# Landing Page
def index(request):
    return render(request, 'main/index.html')

# Filtered Company search table
def searchTable(request):
    return HttpResponse('The search table Page')

# Filter Page
def filter(request):
    return render(request, 'main/filter.html')

# Company summary page
def summary(request, ticker):
    print(ticker.upper())
    company = get_object_or_404(Company, ticker=ticker.upper()) 
    price = company.price_set.latest('ticker_date')
    ratios = company.ratios_set.latest('ticker_date')
    latest_date = company.directors_set.latest('date').date # to get directors, find the date of the latest object in the directors lists. Then, filter the entire list by only the latest date.
    directors = company.directors_set.filter(date = latest_date)
    profile = company.companyprofile_set.latest('ticker_date')
    summary = company.summary_set.latest('ticker_date')
    indices = {
        'netYield': summary.net_dividend_yield_index*100,
        'sharpe': summary.sharpe_ratio_index*100,
        'ROE': summary.return_on_equity_index*100,
        'DE': summary.debt_equity_index*100,

    }
    return render(request, 'main/summary.html', {'company': company, 'price': price, 'profile': profile, 'directors': directors, 'ratios': ratios, 'summary': summary, 'indices': indices})

# Filtered table page
def table(request):
    # take filter dictionary and use that to match strings with the string in the company description
    sinStocks = ['Fuel', 'Alcohol', 'main']
    flag = False
    filteredList = []
    tablefilter = Filter.objects.get(id=1)
    blackList = tablefilter.blacklist.split(', ')
    sinStocks = []
    companyList = Company.objects.all()
    for company in companyList:
        profile = company.companyprofile_set.latest('ticker_date')
        # if any(word in profile.description for word in blackList):
        #     print('SINNER', company.ticker)
        for sin in blackList:
            if re.search(sin, profile.description, re.IGNORECASE):
                print('SINNER', company.ticker)
                sinStocks.append(company)
    companyList = list(companyList)
    for company in sinStocks:
        companyList.remove(company)
    # Can now return companyList as the filtered list
    json_list = []
    for el in companyList:
        # convert model to json
        dict_obj = model_to_dict(el)
        # append price to dict_obj by retrieving the latest market price != 0 (0 means no price change)
        dict_obj['price'] = el.price_set.exclude(price=0).latest('date').price
        dict_obj['marketcap'] = el.summary_set.latest('date').market_cap
        dict_obj['marketcap'] = el.summary_set.latest('date').market_cap
        # append dict to json_list
        json_list.append(json.dumps(dict_obj))
    return render(request,'main/table.html', context={'companies': companyList, 'json_list': json_list, 'test': [1,{'name':'brynn'},3,4,5]})

# add filter information to db
@csrf_exempt
def postfilter(request):
    if request.method == 'POST':
        # data = eval(request.body.decode('utf-8'))
        data = eval(request.body.decode('utf-8'))
        Filter.objects.update_or_create(id=1,defaults={'risk': data['risk'], 'index': data['index'], 'blacklist': data['blacklist']})
        return HttpResponse(data,200)


#confirmation of Scraping
@csrf_exempt #! This is NOT GOOD LONG TERM, WE NEED CSRF SECURITY!!!!!
def update(request):
    if request.method == 'GET':
        return HttpResponse('WRONG TYPE BUCKO, AINT NO GETS AROUND THIS PART OF TOWN')
    if request.method == 'POST':
        if request.FILES:
            saving_data.save_files(request.FILES)
            htmlData = 'You sent some files'
        elif request.body != "":
            data = request.body.decode('utf-8')
            saving_data.save_json_data(data)
            htmlData = 'You sent JSON data!'
        else:
            htmlData = 'You didnt send anything'

        return render(request, 'main/updated.html',{'htmlData': htmlData})

def getPriceData(request, ticker):
    if request.method == 'GET':
        company = get_object_or_404(Company, ticker=ticker.upper()) 
        priceSet = company.price_set.all()[:1095]
        priceJSON = serializers.serialize('json', priceSet)
        return HttpResponse(priceJSON, content_type='application/json')

