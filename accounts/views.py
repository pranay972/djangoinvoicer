from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import F

from .forms import LoginForm, ProductAddForm, BillGenForm, TaxForm

from .models import Product, Bills, BilledProducts, Tax


@login_required
def edit_product_view(request, id):
    instance = get_object_or_404(Product, id = id)

    if request.method == "POST":
        form = ProductAddForm(request.POST or None, instance = instance)
        if form.is_valid():
            form.save()
        return render(request, 'accounts/edit_product_popup.html', {'success' : True})
    else:
        form = ProductAddForm(instance = instance)
        return render(request, 'accounts/edit_product_popup.html', {'form' : form})


#views
@login_required
def all_bill_view(request):
    bills = Bills.objects.all().order_by('-invoice_date')
    return render(request, 'accounts/all_bill.html', {'bills' : bills})


@login_required
def view_bill_view(request, id):
    bill = get_object_or_404(Bills, id = id)
    return render(request, 'accounts/view_bill.html', {'bill' : bill})


@login_required
def gen_bill_view(request):
    form = BillGenForm()
    data = []
    for product in Product.objects.all():
        data.append({
            'name' : product.name,
            'price' : product.price,
            'id' : product.id,
            'inventory' : product.inventory,
            'hsn_code' : product.hsn_code
        })
    import json
    data = json.dumps(data)
    return render(request, 'accounts/bill_gen.html', {'form':form, 'data' : data})


@login_required
def products_view(request, view_data = {}):

    #getting the products
    products = Product.objects.all()
    view_data['products'] = products

    #getting the products add form
    product_add_form = ProductAddForm(view_data.get('form_data'))
    view_data['product_add_form'] = product_add_form

    addition = ""

    if view_data.get('group_success'):
        addition = '#groups'

    return render(request, 'accounts/products.html'+addition, view_data)


@login_required
def index(request):

    if request.method == "POST":
        form = TaxForm(request.POST)
        if form.is_valid():
            if Tax.objects.count() > 0:
                tax = Tax.objects.all()[0]
                tax.tax = form.cleaned_data['tax']
                tax.save()
            else:
                tax = Tax.objects.create(tax = form.cleaned_data['tax'])
                tax.save()

    #get product count
    pc = Product.objects.count()

    #bills count
    bc = Bills.objects.count()

    instance = None
    if Tax.objects.count() > 0:
        instance = Tax.objects.all()[0]

    #tax form
    tax_form = TaxForm(instance = instance)

    return render(request, 'accounts/index.html', {'bill_count' : bc, 'product_count':pc})


def logout_view(request):
    if request.user.is_authenticated():
        from django.contrib.auth import logout
        logout(request)
        return HttpResponseRedirect('/login')
    else:
        raise Http404()


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    invalid = False
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            from django.contrib.auth import authenticate, login
            user = authenticate(username = username, password = password)

            if user is not None:
                login(request, user)

                try:
                    return HttpResponseRedirect(request.GET['next'])
                except:
                    return HttpResponseRedirect('/')

            else:
                invalid = True

    else:

        form = LoginForm()

    return render(request, 'accounts/login.html', {'form' : form, 'invalid': invalid})


# helpers
@login_required
def del_product_helper(request, id):
    if request.method == "POST":
        product = Product.objects.get(pk=id)
        product.delete()
        return redirect('/products', {'product_success' : True})

    else:
        raise Http404()


@login_required
def add_product_helper(request):
    if request.method == "POST":
        data = ProductAddForm(request.POST)
        if data.is_valid():
            product = Product.objects.create(
                name = data.cleaned_data['name'],
                alias = data.cleaned_data['alias'],
                price = data.cleaned_data['price'],
                inventory = data.cleaned_data['inventory'],
                tax = data.cleaned_data['tax']
            )
            product.save()
            return redirect('/products', {'product_success' : True})
        else:
            return render(request, 'accounts/add_product.html', {'form' : data})
    elif request.method == "GET":
        form = ProductAddForm()
        return render(request, 'accounts/add_product.html', {'form' : form})
    else:
        raise Http404()


# apis
def gen_bill(request):
    if request.method == "POST":
        form = BillGenForm(request.POST)
        if form.is_valid():
            bill = Bills.objects.create(
                invoice_date = form.cleaned_data['invoice_date'],
                to = form.cleaned_data['to'],
                collection = form.cleaned_data['collection']
            )

            import json

            billed = json.loads(request.POST['names_gst_and_quantities'])
            billed_list = []
            for x in billed:
                billed_product = BilledProducts.objects.create(
                    name = x['name'],
                    price = x['price'],
                    quantity = x['quantity'],
                    category = int(x['category']),
                    hsn = x['hsn'],
                    bill = bill
                )
                billed_list.append(billed_product)
                print(Product.objects.filter(pk=x['id']).update(
                    inventory=F('inventory') - x['quantity']))
                print(each.inventory for each in Product.objects.filter(pk=x['id']))
            bill.save()
            for b in billed_list:
                b.save()
            return HttpResponse("success#"+str(bill.pk))

        else:
            return HttpResponse(str(form.errors))

    else:
        raise Http404()


def search_product(request, query):
    if request.method == "POST":
        data = []
        for product in Product.objects.filter(name__icontains = query):
            data.append({
                'name' : product.name,
                'alias' : product.alias,
                'price' : product.price
            })
        import json
        data = json.dumps(data)
        return HttpResponse(data)
    else:
        raise Http404()
