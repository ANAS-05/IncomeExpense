from django.contrib.auth.decorators import login_required
from .models import UserIncome,Source
from django.shortcuts import redirect,render
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.contrib import messages
from django.http import JsonResponse


@login_required
def index(request):
    
    incomes = UserIncome.objects.filter(owner = request.user)
    paginator = Paginator(incomes,6)
    page_num = request.GET.get('page') 
    page_obj = Paginator.get_page(paginator,page_num)

    currency = UserPreferences.objects.get(user = request.user).currency 
    
    context = {
        'incomes':incomes,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request,'incomes/index.html',context=context)

@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources' : sources,
        'values' : request.POST
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        income_date = request.POST['income_date']
        source = request.POST['source']
        
        if not amount:
            messages.error(request,'Amount is Required')
            return render(request,'incomes/add-income.html',context=context)
        if not description:
            messages.error(request,'Description is Required')
            return render(request,'incomes/add-income.html',context=context)
        if not income_date:
            messages.error(request,'Date is Required')
            return render(request,'incomes/add-income.html',context=context)
        
        UserIncome.objects.create(owner = request.user, amount=amount,date=income_date,description=description,source=source)
        messages.success(request,'Income saved Successfully')
        return redirect('incomes')

    else:
        return render(request,'incomes/add-income.html',context=context)


def edit_income(request, id):
    return JsonResponse({"test":"this"})

def delete_income(request,id):
    return JsonResponse({"test":"this"})