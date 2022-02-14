import imp
from django.shortcuts import render,redirect

from . forms import *
from . models import Product, Order, Order_item, BillingAddress, Payment

from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    products = Product.objects.all()
    try:
        items = Order_item.objects.filter(user = request.user, ordered = False)
        totalItem = items.count()
    except:
        items = Order_item.objects.all()
        totalItem = items.count()
    context = {
        'products' :products,
        'count':totalItem
    }
    return render(request, 'stores/index.html', context)

def product(request, id):
    try:
        items = Order_item.objects.filter(user = request.user, ordered = False)
        totalItem = items.count()
    except:
        items = Order_item.objects.all()
        totalItem = items.count()
    product = Product.objects.get(id = id)

    context = {
        'product' :product,
        'count':totalItem
    }
    return render(request, 'stores/product.html', context)

#add to cart
@login_required(login_url='login')
def addtocart(request, id):
    item = Product.objects.get(id=id)
    order_item,created = Order_item.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id = item.id).exists():
            order_item.quantity +=1
            order_item.save()
            messages.success(request, f'The quantity updated successfully')
            return redirect(ordersummary)
        else:
            order.items.add(order_item)
            messages.success(request, f'One item added successfully')
            return redirect(product,id=id)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user = request.user,
            ordered_date = ordered_date
        )
        order.items.add(order_item)
        messages.success(request, f'One item added successfully')
        return redirect(ordersummary)

# remove from cart
@login_required(login_url='login')
def removefromcart(request, id):
    item = Product.objects.get(id=id)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id = item.id).exists():
            order_item = Order_item.objects.filter(
            item = item,
            user = request.user,
            ordered = False
            )[0]   
            order.items.remove(order_item)
            messages.info(request, f'Removed from cart successfully')
            return redirect(product,id=id)
        else:
            messages.info(request, f"You Don't have this item in your cart ")
            return redirect(product,id=id)
    else:
        messages.info(request, f"You Don't have any order")
        return redirect(product,id=id)

# remove single item from cart
@login_required(login_url='login')
def removeitemfromcart(request, id):
    item = Product.objects.get(id=id)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id = item.id).exists():
            order_item = Order_item.objects.filter(
            item = item,
            user = request.user,
            ordered = False
            )[0]
            if order_item.quantity >1:
                order_item.quantity -=1
                order_item.save() 
            else:
                order.items.remove(order_item)  
            messages.error(request, f'One item removed successfully')
            return redirect(ordersummary)
        else:
            return redirect(ordersummary)
    else:
        return redirect(ordersummary)

@login_required(login_url='login')
def ordersummary(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        items = Order_item.objects.filter(user = request.user, ordered = False)
        totalItem = items.count()
    except:
        items = Order_item.objects.all()
        totalItem = items.count()
        messages.error(request, f"You don't have any order")
        
    context = {
        'order':order,
        'count':totalItem
    }
    return render(request,'stores/ordersummary.html',context)

# checkout
@login_required(login_url='login')
def checkout(request):
    order = Order.objects.get(user=request.user, ordered=False)
    form = checkoutForm()
    context = {
        'form':form,
        'order':order
    }
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        if request.method == 'POST':
            form = checkoutForm(request.POST)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address') 
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                #TO-DO: adding the function of saving billing address
                save_billing_address = form.cleaned_data.get('save_billing_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                
                billing_address = BillingAddress(
                    user = request.user,
                    street_address = street_address,
                    apartment_address =apartment_address,
                    country =country,
                    zip =zip,

                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                if payment_option == 'Paypal':
                    return redirect('payment', payment_option='paypal')
                elif payment_option == 'Paystack':
                    return redirect('payment', payment_option='paystack')
                else:
                    messages.error(request, f'Invalid Payment Option')
                    return render(request, 'stores/checkout.html',context)
            else:             
                return render(request, 'stores/checkout.html',)
        messages.error(request, f'Failed To Checkout')
    except:
        messages.error(request, f'No Order to checkout')
        return redirect('ordersummary')

    return render(request,'stores/checkout.html',context)

@login_required(login_url='login')
def paymentPage(request, payment_option):
    order = Order.objects.get(user=request.user, ordered=False)
    payment = Payment()

    payment.user = request.user
    payment.email = request.user.email
    payment.amount = order.get_total()
    payment =payment.save()
    order.ordered = True
    order.payment = payment
    order.save()
    if payment.verified:
        payment.verified = True
        messages.error(request, f'Payment SUccessful')
        return redirect('dashboard')

    return render(request,'stores/payment.html',{'payment':payment,'order':order})

