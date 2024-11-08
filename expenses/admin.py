from django.contrib import admin,messages

from .models import Expense,Category
# Register your models here.

admin.site.site_header = "Admin Portal"
admin.site.index_title = "Welcome to the Admin Dashboard"


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['amount','description','owner','category','date']    
    search_fields = ['description','date','amount','category']
    list_per_page = 5
    list_filter = ['date']


admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Category)