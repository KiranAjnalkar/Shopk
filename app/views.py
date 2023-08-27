from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Contact, Customer, Product, Cart, OrderPlaced
from  .forms import  CustomerProfileForm 
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  
from django.utils.decorators import method_decorator       
from .models import Product
from .tokens import generate_token
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from shopk import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
import json
import requests
from .config import RECAPTCHA_SECRET_KEY



class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        topoffers = Product.objects.filter(category='TO')

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'home.html', {'topwears':topwears, 'bottomwears': bottomwears, 'mobiles' :mobiles, 'laptops' :laptops, 'topoffers': topoffers, 'totalitem': totalitem} )



class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product = product.id) & Q(user = request.user)).exists()
        return render(request, 'productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem} )



@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 50.00
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]   
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'addtocart.html', {'carts':cart, 'totalamount': totalamount, 'amount': amount, 'totalitem': totalitem} )
        else:  
            return render(request, 'emptycart.html')
        


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()

            cart_product = Cart.objects.filter(user=request.user)
            amount = sum(p.quantity * p.product.discounted_price for p in cart_product)
            shipping_amount = 50.00
            totalamount = amount + shipping_amount

            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Item not found in cart'})
        


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()

        if cart_item:
            cart_item.quantity -= 1
            cart_item.save()

            cart_product = Cart.objects.filter(user=request.user)
            amount = sum(p.quantity * p.product.discounted_price for p in cart_product)
            shipping_amount = 50.00
            totalamount = amount + shipping_amount

            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Item not found in cart'})



def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()

        if cart_item:
            cart_item.delete()

            cart_product = Cart.objects.filter(user=request.user)
            amount = sum(p.quantity * p.product.discounted_price for p in cart_product)
            shipping_amount = 50.00
            totalamount = amount + shipping_amount

            data = {
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Item not found in cart'})



@method_decorator(login_required, name='dispatch')  
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'profile.html', {'form':form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user                 
            name = form.cleaned_data['name']
            mobile_number = form.cleaned_data['mobile_number']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, mobile_number=mobile_number, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request,'Your Profile is Updated!')
        return render(request, 'profile.html', {'form': form, 'active': 'btn-primary'} )



@login_required
def address(request):
    totalitem = 0
    add = Customer.objects.filter(user=request.user)  
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
          
    return render(request, 'address.html', {'add': add, 'active' : 'btn-primary', 'totalitem': totalitem})



@login_required
def orders(request):
    totalitem = 0
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    
    return render(request, 'orders.html', {'order_placed' :op, 'totalitem': totalitem} )



def mobile(request, data=None):
    totalitem = 0
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Vivo' or data == 'Oppo' or data =='Apple' or data == 'OnePlus'  or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000) 
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000) 
    
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    
    return render(request, 'mobile.html', {'mobiles' :mobiles, 'totalitem': totalitem} )



def laptop(request, data=None):
    totalitem = 0
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Lenovo' or data == 'Dell' or data == 'HP':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=50000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=50000)
    
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'laptop.html', {'laptops' :laptops, 'totalitem' :totalitem})



def topwear(request, data=None):
    totalitem = 0
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Ketch' or data == 'Nancy' or data == 'Lee':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=500)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=500)

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'topwear.html', {'totalitem': totalitem, 'topwears': topwears})



def bottomwear(request, data=None):
    totalitem = 0
    if data == None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'Lee' or data == 'Ketch':
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=500)
    elif data =='above':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=500)
    
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'bottomwear.html', {'bottomwears':bottomwears, 'totalitem':totalitem})



def top_offers(request):
    totalitem = 0
    topoffers = Product.objects.filter(category='TO')
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
    return render(request, 'top_offers.html', {'topoffers': topoffers, 'totalitem': totalitem} )



@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)  
    Cart(user=user, product=product).save()
    return redirect('/cart')



@login_required
def buynow(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    if user.is_authenticated:
        cart_item = Cart.objects.get_or_create(user=user, product=product)
        if not cart_item:
            cart_item.quantity += 1
            cart_item.save()
            
        return redirect('checkout')
    else:
        return redirect('login')



@login_required    
def checkout(request):
    totalitem = 0
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 50.00
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product: 
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'checkout.html', {'add': add, 'totalamount' : totalamount, 'cart_items' : cart_items, 'totalitem': totalitem})



@login_required    
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()

    return redirect("orders")



def about(request):
    return render(request, 'about.html')



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        # Recaptcha
        clientkey = request.POST.get('g-recaptcha-response')
        secretkey = RECAPTCHA_SECRET_KEY
        captchaData = {
            'secret': secretkey,
            'response': clientkey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response.get('success', False)
        if verify:
            contact = Contact(name=name, email=email, desc=desc, date=datetime.today())
            contact.save()
            messages.success(request, 'Your message has been sent!')
        else:
            messages.error(request, 'reCAPTCHA verification failed. Please try again.')

    return render(request, 'contact.html')



def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # Recaptcha
        clientkey = request.POST.get('g-recaptcha-response')
        secretkey = RECAPTCHA_SECRET_KEY
        captchaData = {
            'secret': secretkey,
            'response': clientkey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['success']  
        if verify:
            if User.objects.filter(username=username):
                messages.error(request, "Username already exist! Please try some other username.")
                return redirect('home')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email Already Registered!!")
                return redirect('home')
            
            if len(username)>20:
                messages.error(request, "Username must be under 20 charcters!!")
                return redirect('home')
            
            if pass1 != pass2:
                messages.error(request, "Passwords didn't matched!!")
                return redirect('home')
            
            if not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric!!")
                return redirect('home')
            
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()
            messages.success(request, "Your Account has been created successfully!! Please check your email to confirm your email address in order to activate your account.")
            
            # Welcome Email  ( Its an 1st mail )
            subject = "Welcome to ShopK!!"
            message = "Hello " + myuser.first_name + "!!\n" + "Welcome to ShopK!!\nThank you for visiting our Shop.\nWe have also sent you a confirmation email, please confirm your email address.\nThank You,\nTeam ShopK"        
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            
            # Email Address Confirmation Email   ( Its an 2nd mail )
            current_site = get_current_site(request)
            email_subject = "Confirm your Email @ ShopK - Login!!"
            message2 = render_to_string('email_confirmation.html',{
                
                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
            )
            email.fail_silently = True
            email.send()
            
            return redirect('/')
        
    return render(request, "signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('profile')
    else:
        return render(request,'activation_failed.html')



def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # Recaptcha
        clientkey = request.POST.get('g-recaptcha-response')
        secretkey = RECAPTCHA_SECRET_KEY
        captchaData = {
            'secret': secretkey,
            'response': clientkey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['success']  
        if verify:
            # Check if user has entered correct credentials.
            user = authenticate(username=username, password=password)
            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                return redirect("/")
            else:
                # No backend authenticated the credentials
                return render(request, 'login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'login.html')



def search(request):
    query = request.GET.get('search', '')

    product = Product.objects.filter(
        Q(title__icontains=query) |
        Q(brand__icontains=query) |
        Q(category__icontains=query)
    )

    return render(request, 'search.html', {'product': product})



@method_decorator(login_required, name='dispatch')  
class Update(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,'update.html',{'form':form})
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():  
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.mobile_number = form.cleaned_data['mobile_number']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")

