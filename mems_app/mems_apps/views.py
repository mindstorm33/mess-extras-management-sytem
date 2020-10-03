from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate ,login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import F


from .models import *
from .forms import MessExtrasForm, OrderForm


# Create your views here.
def index(request):
    """ The home page for mems  for admins """

    avail_extras = MessExtra.objects.all()
    context = {'avail_extras' : avail_extras}
    return render(request,'mems_apps/index.html', context)

@login_required
def new_extra(request):
    """ render page for admin to add exras to the menu """

    if request.method != 'POST':
    #    No data submitted; create blank form.
        form = MessExtrasForm()
    else:
        # POST data submitted; process data.
        form = MessExtrasForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('mems_apps:index'))
    
    context = {'form' : form }
    return render(request,'mems_apps/new_extra.html',context)

@login_required
def remove_extra(request,extra_id):
    """ remove selected extra """

    extra = MessExtra.objects.get(id=extra_id)
    extra.delete()
    return HttpResponseRedirect(reverse('mems_apps:index'))


@login_required
def todays_orders(request):
    """ render page for showing admin the current days 'order' info """

    orders = Record.objects.all()
    context = {'orders': orders }
    return render(request, 'mems_apps/todays_orders.html', context)

# ===================================================================
# this is just a quick fix; student users' views will be moved a separate app later

def student_register(request):
    """Register a new student user """

    if request.method != 'POST':
        # Display blank registration form.
        form = UserCreationForm()
    else:
        # Process complete form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # log the student in and then redirect to student_index
            authenticated_user = authenticate(username=new_user.username,
                                password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('mems_apps:student_index'))
    
    context = {'form': form }
    return render(request,'mems_apps/student_register.html', context)


def logout_view(request):
    """Log the student User out"""
    logout(request)
    return HttpResponseRedirect(reverse('mems_apps:student_login'))


def student_index(request):
    """ render home page for student user """
    
    avail_extras = MessExtra.objects.all()
    selected_extras = Order.objects.filter(student=request.user)

    context = {'avail_extras' : avail_extras, 'selected_extras': selected_extras}
    return render(request,'mems_apps/student_index.html', context)

@login_required
def add_to_plate(request):
    """ render page where student user will select what to add to 'plate' """

    if request.method != 'POST':
        # No data submitted; create blank form
        form = OrderForm()
    else:
        # POST data submitted; process data
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order_request = form.save(commit=False)
            new_order_request.student = request.user
            form.save()
            return HttpResponseRedirect(reverse('mems_apps:see_plate'))

    context = {'form': form}
    return render(request,'mems_apps/add_to_plate.html', context)

@login_required
def remove_from_plate(request,order_id):
    """remove selected extra from plate """

    order = Order.objects.get(id=order_id)
    order.delete()
    return HttpResponseRedirect(reverse('mems_apps:see_plate'))

@login_required
def see_plate(request):
    """ a summary of what the user has selected """
    selected_extras = Order.objects.filter(student=request.user)

    context = {'selected_extras': selected_extras}
    return render(request,'mems_apps/see_plate.html', context)



@login_required
def confirmation(request):
    """ confirmation page """

    # action 1 : update the number of available coupons
    sel_extras = Order.objects.filter(student=request.user)

    for sel_extra in sel_extras:
        ex_up = MessExtra.objects.get(id=sel_extra.extras_type.id)
        ex_up.quantity = F('quantity') - sel_extra.quantity
        ex_up.save()

    # action 2: update records

    # action 3: empty plate (remove selected extras from page)
    orders = Order.objects.filter(student=request.user)
    for order in orders:
        record = Record.objects.create(
            student_id = order.student_id,
            order_id = order.id,
            quantity = order.quantity,
            amount = order.quantity * order.extras_type.price,
            food_name = order.extras_type.name
        )
        order.delete()
    
    # action 4: render confirmation page(THIS NEEDS ADJUSTING!!)
    context = {'sel_extras': sel_extras,}
    return render(request, 'mems_apps/confirmation.html', context)

@login_required
def see_totals(request):
        """ render page that shows the user a summary of all her orders """
        records = Record.objects.filter(student_id=request.user.id)
        total_amount = 0.0
        for record in records:
            total_amount = total_amount + int(record.amount)

        context = {'records': records, 'total_amount':total_amount }
        return render(request,'mems_apps/see_totals.html',context)





