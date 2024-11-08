from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreferences
from django.contrib import messages
# Create your views here.

def index(request):
    
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR,'currency.json')

    with open(file_path,'r') as json_file:
        
        data = json.load(json_file)
        for currency in data:
            code = currency['cc']
            symbol = currency['symbol']
            name = currency['name']

            currency_data.append({'code':code ,'name':name , 'symbol':symbol })


    # Python Debugger
    # import pdb
    # pdb.set_trace()
    

    # Check if user preferences already exist
    user_preferences = None
    exists = UserPreferences.objects.filter(user = request.user).exists()
    if exists:
        user_preferences = UserPreferences.objects.get(user = request.user)



    if request.method == 'GET':    
        return render(request,'preferences/index.html',context={'currencies':currency_data,'user_preferences':user_preferences})
    
    else:   
        #POST METHOD
        currency = request.POST['currency']
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreferences.objects.create(user = request.user , currency = currency)

        messages.success(request,'Changes Saved')
        return render(request,'preferences/index.html',context={'currencies':currency_data,'user_preferences':user_preferences})