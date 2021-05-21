from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Product, Order, Item, Shopper
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Max

#------------------------------------------------------------------------------
@login_required
def index(request):
    """ Get a list of all products from the database. """

    product_objects = Product.objects.all().order_by('category','title')
    item_name = request.GET.get('item_name')

    if item_name is None and 'item_name' in request.session:
        item_name = request.session['item_name']
    request.session['item_name'] = item_name

    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(title__icontains=item_name)

    paginator = Paginator(product_objects, 4)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)

    # Store the current page so that the detail page can return here.
    if page is None: request.session['page'] = 1
    else: request.session['page'] = page

    return render(request, 'shop/index.html', {'product_objects':product_objects})

#------------------------------------------------------------------------------
@login_required
def detail(request, id):

    product_object = Product.objects.get(id=id)
    # Calculate the customer's saving on this item.
    saving = round(product_object.price - product_object.discount_price, 2)

    # Retrieve the page number of the product list to return to.
    if 'page' in request.session:
        page = request.session['page']
    else:
        page = 1

    return render(request, 'shop/detail.html',
        {'product_object':product_object, 'saving':saving, 'page':page})

#------------------------------------------------------------------------------
@login_required
def checkout(request):
    """ Display the cart checkout page and save order details.  """
    import json

    cust = Shopper.objects.filter(userid = request.user.id)
    if request.method == 'POST':
        items = request.POST.get('items','')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address = request.POST.get('address','')
        district = request.POST.get('district','')
        city = request.POST.get('city','')
        county = request.POST.get('county','')
        postcode = request.POST.get('postcode','')

        if not cust:
            cust = Shopper.objects.create(
                name=name.title(), email=email,
                address=address.title(), district=district.title(),
                city=city.title(), county=county.title(),
                postcode=postcode.upper(), userid=request.user.id  )
        else:
            cust = Shopper.objects.filter(userid=request.user.id)\
                .update(name=name.title(), email=email,
                address=address.title(), district=district.title(),
                city=city.title(), county=county.title(),
                postcode=postcode.upper())
            cust = Shopper.objects.get(userid=request.user.id)
 
        new_order = Order.objects.create(userid=cust)

        # Get a Python dictionary from the JSON string
        prods = json.loads(items)
        if len(prods) == 0: return redirect('index')
        storeItems(prods, new_order)

        # Get a list of order ids where userid = current user id.
        orders = list(Order.objects.filter(userid=request.user.id)\
                    .values_list('pk', flat=True))

        # Get all order items for the current user.
        items = Item.objects.filter(order_id__in=orders)

        # Group the order items and get sums, etc.
        history = items.values('order__id')\
                .annotate(Sum('cost'),Sum('quantity'),Max('order__orderdate'))\
                .order_by('-order__id')

        for num in history: num['cost__sum'] = round(num['cost__sum'],2)
        return render(request,'shop/confirm.html', {'name':', ' + name,'history':history})

    if cust:
        return render(request, 'shop/checkout.html', {'cust':cust[0]})
    else:
        return render(request, 'shop/checkout.html')

#------------------------------------------------------------------------------
@login_required
def confirm(request):
    """ Order confirmation screen. """

    return render(request, 'shop/confirm.html')

#------------------------------------------------------------------------------
login_required
def orders(request):
    """ List all orders for the specified customer. """

    # Get a list of order ids where userid = current user id.
    orders = list(Order.objects.filter(userid=request.user.id)\
                .values_list('pk', flat=True))

    # Get all order items for the current user.
    items = Item.objects.filter(order_id__in=orders).order_by('-order_id')

    return render(request, 'shop/orders.html', {'history':items})

#------------------------------------------------------------------------------
def storeItems(items, new_order):
    """ Extract the individual order items, and write them to the Item
        database table. """

    for idx in items:
        prod_id = int(idx)      # fk to Product table
        quant = items[idx][0]
        cost = items[idx][2]
        product = Product.objects.get(id=prod_id)

        new_item = Item(item=product, quantity=quant, cost=cost, order=new_order)
        new_item.save()

#------------------------------------------------------------------------------
@login_required
def history(request, order_id):
    """ Display full details of the requested order selected from the list of
        previous orders. Only displays the one order, with options to either
        go back to the history list or back to the home screen.  """

    order = Order.objects.get(id=order_id)
    items = Item.objects.filter(order=order)

    return render(request, 'shop/history.html', {'order_ref':order_id,'order':items})

#------------------------------------------------------------------------------