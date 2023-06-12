from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from .admin import RepairForm
from .models import Repair, Brand
from django.shortcuts import render
from .forms import RepairForm
from django.shortcuts import render
from django.db.models import Q
from .models import Repair


import json
from pathlib import Path
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.files.storage import default_storage
from django.urls import reverse

from .forms import RepairForm
from .models import *
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .serialzers import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

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



def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass1']
        extra_fields = {}
        first_name = request.POST['fname']

        last_name = request.POST['lname']
        location = request.POST['location']
        nbre = request.POST['nbre']
        Users = get_user_model()
        myuser = Users.objects.create(username= username,
                                     email=email,
                                     first_name=first_name,last_name=last_name,location=location, number = nbre)
        myuser.set_password(password)

        myuser.save()

        messages.success(request,"Your account has been successfully created!")
        return redirect('signin')

    elif request.method =="GET":
        return render(request,"authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass1']
        # Provide the authentication backend for your custom user model
        backend = 'ZapNFixApp.backends.YourCustomUserModelBackend'

        user = authenticate(request,username=username,password=password)
        if user != None:
            login(request,user)
            fname=user.first_name
            if fname is not None:
             return render(request,'index.html',{'fname':fname})
            else:
                return render(request, 'index.html', {'fname': ""})
        elif user is None:
            messages.error(request, "Wrong Credentials!")
            return redirect('signin')
    elif request.method =="GET":
       return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"you have been successfully logged out!")
    return render(request, 'index.html')

@csrf_exempt
def ClientRepairApi(request,id=0):

    if request.method == "GET":
      if request.user.is_authenticated:
        repairs = Repair.objects.all()
        repairs_serializer = RepairSerializer(repairs,many=True)
        context = {}
        context["dataset"] = repairs
        return render(request, "Repairs.html", context)
        #return JsonResponse(repairs_serializer.data,safe=False)
      else:
          messages.error(request, "Please Sign In first!")
          return render(request, 'index.html')
    elif request.method == "POST":
        repairs_data = JSONParser().parse(request)
        repairs_serializer = RepairSerializer(data=repairs_data)
        if repairs_serializer.is_valid():
            repairs_serializer.save()

            return JsonResponse("Repair Requested successfully!",safe=False)
        return JsonResponse("Repair wasn't created successfully!" + str(repairs_serializer),safe=False)
    elif request.method == 'PUT':
        repair_data = JSONParser().parse(request)
        #Might need to change it to id
        repair = Repair.objects.get(id=repair_data['id'])
        repair_serializer = RepairSerializer(repair, data=repair_data)
        if repair_serializer.is_valid():
            repair_serializer.save()
            return JsonResponse("Repair Updated successfully!", safe=False)
        return JsonResponse("Repair wasn't updated successfully!", safe=False)

    elif request.method == 'DELETE':
       try:
          repair_data = JSONParser().parse(request)
          repair = Repair.objects.get(id=repair_data['id'])
          repair.delete()
          return JsonResponse({"message": "Repair Deleted Successfully"}, safe=False)
       except Repair.DoesNotExist:
          return JsonResponse({"message": "Repair not found"}, status=404, safe=False)

def Feeback(request,id):
    if request.method == "POST":

        repair = get_object_or_404(Repair, id=id)

        bodyString = request.body.decode('utf-8')
        body = json.loads(bodyString)
        rate = body['rate'] # Retrieve the rating value from the POST data
        notes = body['notes']
        print(notes)
        if rate != None:
             repair.feedbackRate = rate
             repair.notes = notes
             #repair.notes = request['notes']
             repair.save()
             redirect_url = reverse('RepairList')
             return HttpResponse("Success")

        else:
            redirect_url = reverse('RepairList')
            # Redirect to a success page or do further processing
            messages.error(request,"OOps, Your feedback was not saved, Please try again later!:)")
            print("rate is empty?")
            print(request.POST)
            for key, value in request.POST.items():
                print(f"{key}: {value}")
            #return redirect(redirect_url)
            return HttpResponse("Error")

    elif request.method == "GET":
        context = {}
        print("repair_id" + str(id))
        repairs = get_object_or_404(Repair,id=id)
        context["dataset"] = repairs

        return render(request, "Feedback.html", context)


def ClientRepairDelete(request,id):
            repair = get_object_or_404(Repair,id=id)
            repair.delete()
            messages.success(request, "you have been successfully logged out!")
            redirect_url = reverse('RepairList')
            return redirect(redirect_url)

def addRequest(request):
    if request.method == 'GET':
      if  request.user.is_authenticated :
        Types = Type.objects.all()
        Brands = Brand.objects.all()
        brandSerializer =  BrandSerializer(data=Brands,many=True)
        typeSerializer = TypeSerializer(data=Types, many=True)
        context = {
            'Types': Types,
            'Brands': Brands,
        }

        for type in Types:
            print('type' + type.desc)
        for brand in Brands:
            print('type' + brand.desc)
        return render(request,'AddRequest.html',context)
      else:
          messages.error(request, "Please Sign In first!")
          render('home')
    if request.method == 'POST':
        user = request.user
        desc = request.POST['desc']
        isDelivery = request.POST['isDelivery']
        brand = get_object_or_404(Brand, id=request.POST['product_id'])
        image = request.FILES['image']
        print(str(image))
        myRequest = Repair.objects.create(desc=desc,
                                      isDelivery=isDelivery,
                                      image=image, user_idClient=user, product_id = brand)

        myRequest.save()
        messages.success(request, "Your Image has been successfully added!")
        return redirect('home')
    else:
        form = RepairForm()
        return render(request, 'AddRequest.html', {'form': form} )

def addPicture(request):
    if request.method == 'POST':

        form = RepairForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Your Image has been successfully added!")
            return redirect('AddRequest')
    else:

        form = RepairForm()
    return render(request, 'AddRequest.html', {'form': form})

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@ensure_csrf_cookie
def FilterBrand(request):
    if request.method == 'GET' and is_ajax(request):
        type_id = request.GET.get('type_id')

        # Perform the filtering based on type_id
        filtered_brands = Brand.objects.filter(type_id=type_id)

        # Create a list of filtered brand data
        for brand in filtered_brands:
            print( str(brand.id ))
        filtered_data = [{'desc': brand.desc, 'id': brand.id} for brand in filtered_brands]

        return JsonResponse(filtered_data, safe=False)

    # Handle other cases if needed
    return JsonResponse({'message': 'Invalid request'})
@csrf_exempt
def SavePhoto(request):
    pass
# Needs update actually

