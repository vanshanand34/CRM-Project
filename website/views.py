from django.shortcuts import render , redirect
from django.contrib.auth import login , logout , authenticate
from django.contrib import messages
from .forms import SignUpForm , AddRecordForm
from .models import Record
# Create your views here.

def home(request):
    records = Record.objects.all()
    if request.method=='POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request , "You have been logged in")
            return redirect('home')
        else:
            messages.success(request,"There Was An Error Logging In , Please Try Again.......")
            return redirect('home')
    return render(request,'home.html',{'records':records})


def register_user(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request,username=username , password = password)
            login(request , user)
            messages.success(request,"You have been successfully registered ! Welcome onboard !")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request,'register.html',{'form':form})
    return render(request,'register.html',{'form':form })

def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out ... ")
    return redirect('home')

def customer_record(request,pk):
    if request.user.is_authenticated:
        crecord = Record.objects.get(id=pk)
        return render(request,'customer.html',{'crecord':crecord })
    else:
        messages.info(request,"You have to be logged in to view this page!")
        return redirect('home')
    
def delete_record(request,pk):
    if request.user.is_authenticated:
        crecord = Record.objects.get(id=pk)
        crecord.delete()
        messages.success(request,"Record deleted Successfully !!!")
        return redirect('home')
    else:
        messages.info(request,"You MUST BE logged in to do this ....")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method=='POST':
            if form.is_valid():
                addmyrecord = form.save()
                messages.success(request,"Record added successfully")
                return redirect('home')
        return render(request,'add_record.html',{'form':form})
    else:
        messages.info(request,"You must be logged in to add a record")
        return redirect('home')
    

def update_record(request,pk):
    if request.user.is_authenticated:
        current = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None , instance=current)
        if form.is_valid():
            form.save()
            messages.success(request,"Record Updated Successfully")
            return redirect('home')
        return render(request,'update_record.html',{'form':form}) 
    else:
        messages.info("You must be logged in to Update a record")
        return redirect('home')

