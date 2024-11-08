import json
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Expense,Category
from django.http import JsonResponse
from userpreferences.models import UserPreferences 
import datetime
# Create your views here.

@login_required
def index(request):
    
    expenses = Expense.objects.filter(owner = request.user)
    paginator = Paginator(expenses,6)
    page_num = request.GET.get('page') 
    page_obj = Paginator.get_page(paginator,page_num)

    context = {
        'expenses':expenses,
        'page_obj':page_obj
    }
    
    if(UserPreferences.objects.filter(user = request.user)):
        currency = UserPreferences.objects.get(user = request.user).currency 

        # Adding currency in context if exists
        context['currency'] = currency
    
    return render(request,'expenses/index.html',context=context)

@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
        'values' : request.POST
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        expense_date = request.POST['expense_date']
        category = request.POST['category']
        
        if not amount:
            messages.error(request,'Amount is Required')
            return render(request,'expenses/add-expense.html',context=context)
        if not description:
            messages.error(request,'Description is Required')
            return render(request,'expenses/add-expense.html',context=context)
        if not expense_date:
            messages.error(request,'Date is Required')
            return render(request,'expenses/add-expense.html',context=context)
        
        Expense.objects.create(owner = request.user, amount=amount,date=expense_date,description=description,category=category)
        messages.success(request,'Expense created Successfully')
        return redirect('expenses')

    else:
        return render(request,'expenses/add-expense.html',context=context)

@login_required(login_url='/authentication/login')
def edit_expense(request,id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense' : expense,
        'categories' : categories
    }
    if request.method == 'GET':
        return render(request,'expenses/edit-expense.html',context=context)
    else:
        amount = request.POST['amount']
        description = request.POST['description']
        expense_date = request.POST['expense_date']
        category = request.POST['category']
        
        if not amount:
            messages.error(request,'Amount is Required')
            return render(request,'expenses/edit-expense.html',context=context)
        if not description:
            messages.error(request,'Description is Required')
            return render(request,'expenses/edit-expense.html',context=context)
        if not expense_date:
            messages.error(request,'Date is Required')
            return render(request,'expenses/edit-expense.html',context=context)
        
        expense.amount=amount
        expense.date=expense_date
        expense.description=description
        expense.category=category
        expense.save()

        messages.success(request,'Edit Successfull')
        return redirect('edit-expense', id=expense.id)
    
    
def delete_expense(request,id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request,'Expense Deleted Successfully')
    return redirect('expenses')


def search_expenses(request):
    if request.method == 'POST':
           
       search_string = json.loads(request.body).get('searchText')

       #Django provides a rich set of field lookups that allow you to filter querysets in various ways.
       expenses =  Expense.objects.filter(
        owner=request.user,amount__startswith=search_string) | Expense.objects.filter(
        owner=request.user,date__startswith=search_string) | Expense.objects.filter(
        owner=request.user,description__icontains=search_string) | Expense.objects.filter(
        owner=request.user,category__icontains=search_string)
    
       data = expenses.values()
       return JsonResponse(list(data),safe=False)
    
    else:
       return redirect('expenses')


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, #gte -> greater than equal to
                                      date__lte=todays_date)    #lte -> less than equal to

    finalrep = {}

    def get_category(expense):
        return expense.category
    
    category_list = list(set(map(get_category, expenses)))  #The map() function in Python is used to apply a given function to each item in an iterable (like a list, tuple, etc.) and return a map object (which is an iterator) that produces the results.

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for y in category_list:
        finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')