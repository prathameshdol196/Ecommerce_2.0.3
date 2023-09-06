from django.shortcuts import render, redirect
from app.models import slider, banner_area, Main_Category, Product, Category, Color, Brand

from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.http import JsonResponse

from django.db.models import Max, Min, Sum

from django.contrib.auth.decorators import login_required
from cart.cart import Cart


def BASE(request):
    return render(request, 'base.html')


def HOME(request):
    sliders = slider.objects.all().order_by('-id')[0:3]
    banners = banner_area.objects.all().order_by('-id')[0:3]

    main_category = Main_Category.objects.all()

    product = Product.objects.filter(section__name='Top Deals Of The Day')

    context = {
        'sliders': sliders,
        'banners': banners,
        'main_category': main_category,
        'product': product,
    }
    return render(request, 'main/home.html', context)


def PRODUCT_DETAILS(request, slug):
    product = Product.objects.filter(slug=slug)

    if product.exists():
        product = Product.objects.get(slug=slug)
    else:
        return redirect('404')

    context = {
        'product': product,
    }
    return render(request, 'product/product_detail.html', context)


def ERROR404(request):
    return render(request, 'errors/404.html')


@login_required(login_url="/accounts/login/")
def MY_ACCOUNT(request):
    return render(request, 'account/my-account.html')


def REGISTER(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists!")
            return redirect("login")

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email already exists!")
            return redirect("login")

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()

        return redirect("login")


def LOGIN(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Email or Password is Invalid!")
            return redirect('login')


@login_required(login_url="/accounts/login/")
def PROFILE(request):
    return render(request, "profile/profile.html")


def ABOUT(request):
    return render(request, "main/about.html")


def CONTACT(request):
    return render(request, "main/contact.html")


def PRODUCT(request):

    category = Category.objects.all()
    product = Product.objects.all()

    color = Color.objects.all()

    brand = Brand.objects.all()

    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))

    FilterPrice = request.GET.get('FilterPrice')
    COLORID = request.GET.get("colorID")

    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte=Int_FilterPrice)
    elif COLORID:
        product = Product.objects.filter(color=COLORID)
    else:
        product = Product.objects.all()

    context = {
        "category": category,
        "product": product,
        "min_price": min_price,
        "max_price": max_price,
        "FilterPrice": FilterPrice,
        "color": color,
        "brand": brand,
    }
    return render(request, "product/product.html", context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    product_num = request.GET.getlist("product_num[]")
    brand = request.GET.getlist("brand[]")


    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()


    if len(product_num) > 0:
        allProducts = allProducts.all().orderby("-id")[0:1]

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()

    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):

    cart = request.session.get('cart')

    packing_cost = sum(i["packing_cost"] for i in cart.values() if i)
    tax = sum(i["tax"] for i in cart.values() if i)

    # packaging_cost
    # tax
    # print("##########")
    # print(cart)
    # print("#############")
    #
    #
    # print(packing_cost, tax)
    context = {
        "packing_cost": packing_cost,
        "tax": tax,
    }

    return render(request, 'cart/cart.html', context)


@login_required(login_url="/accounts/login/")
def CHECKOUT(request):

    cart = request.session.get('cart')
    packing_cost = sum(i["packaging_cost"] for i in cart.values() if i)
    tax = sum(i["tax"] for i in cart.values() if i)


    packing_and_tax_cost = (packing_cost + tax)

    context = {
        "packing_and_tax_cost": packing_and_tax_cost
    }
    return render(request, "checkout/checkout.html", context)