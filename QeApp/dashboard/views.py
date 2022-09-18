from django.shortcuts import render, redirect
from django .forms import inlineformset_factory

# Create your views here.
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from .filters import OrderFilter


def home(request):
     customer= Customer.objects.all()
     orders= Order.objects.all()
     totalorders= orders.count()
     odelivered= orders.filter(status='Delivered').count()
     opending= orders.filter(status='Pending').count()
     context= {'customers':customer, 'orders':orders,'totalorders':totalorders,'odelivered':odelivered,'opending':opending}
     return render(request, 'dashboard/home.html',context)
   

def customer(request, pk_test):
    
    customer = Customer.objects.get(id=pk_test)
    
    orders = customer.order_set.all()
    order_count = orders.count()
    
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    
    context ={ 'customer': customer, 'orders': orders, 'order_count': order_count, 'myFilter': myFilter }
    
    return render(request, 'dashboard/customer.html',context)

def product(request):
    
    products = Product.objects.all()
    
    return render(request, 'dashboard/product.html',{'products':products})

def createOrder(request,pk):
    
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'),extra=5)
    customer =Customer.objects.get(id=pk)   
    formset =OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    
    context ={'formset':formset}
    
    return render(request, 'dashboard/order_form.html', context)


def updateOrder(request,pk):
    
    
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {'form': form}
    return render(request, 'dashboard/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method =="POST":
         order.delete()
         return redirect('/')
    context={'item': order}
    return render(request, 'dashboard/delete.html',context) 