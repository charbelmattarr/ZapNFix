from django.shortcuts import render, get_object_or_404, redirect

from .admin import RepairForm
from .models import Repair
from django.shortcuts import render
from .forms import RepairForm
from django.shortcuts import render
from django.db.models import Q
from .models import Repair


def index_page(request):
    repairs = Repair.objects.all()
    print("tested")
    print(repairs)

    # Pass data to the template
    context = {'repairs': repairs}
    return render(request, 'index.html',context)

def list_page(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            repairs = Repair.objects.all()
            context = {}
            context["dataset"] = repairs
            return render(request, "list.html", context)


def repair_list_search(request):
    query = request.GET.get('q')  # Get the search query from the request
    data = Repair.objects.all()

    if query:
        # Filter the repairs based on the search query
        data = data.filter(
            Q(desc__icontains=query) |
            Q(status__icontains=query) |
            Q(repairDate__icontains=query)
        )
    context={}
    context["dataset"] = data
    return render(request, 'list.html', context)
def ClientRepairEdit(request, id):
    repair = get_object_or_404(Repair, id=id)
    print("Client Repair Edit ")
    if request.method == 'POST':
        print("Client Repair POST: "+ str(request.method))
        form = RepairForm(request.POST, instance=repair)
        #print("data: "+str(form.cleaned_data))
        print("before formIsValid")
        if form.is_valid():
            print("Client Repair is Valid")
            form.save()
            # Redirect to a success page or render a response
            return redirect('list')
        else:
            print("errorr: "+str(form.errors))
    else:
        print("Client Repair GET")
        form = RepairForm(instance=repair)

    print("Client Repair else")
    context = {'form': form}
    return render(request, 'edit_repair.html', context)

# views.py


def ClientRepairDelete(request, id):
    repair = get_object_or_404(Repair, id=id)
    repair.delete()
    return redirect('list')


def services_page(request):
    return render(request, 'services.html')
