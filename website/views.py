from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm,AddRecordForm
from .models import Record
# Create your views here.


def home(request):
    records = Record.objects.all()
    # check to see if logging in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in ")
            return redirect("home")
        else:
            messages.success(request, "There was an error to logging you in , try again later")
            return redirect("home")
    else:
        return render(request, 'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out...")
    return redirect("home")

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # authenticate and login
            username = form.cleaned_data('username')
            password = form.cleaned_data('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been successfully registered! Welcome!")
            return redirect('home')
    
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def customer_records(request, pk):
     if request.user.is_authenticated:
         #Look up the saved records
         customer_records = Record.objects.get(id=pk)
         return render(request, 'record.html', {'customer_records': customer_records})
     else:
            messages.success(request, "You have to login to see records")
            return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record successfully deleted!")
        return redirect('home')
    else:
        messages.success(request, "You have to login to Delete records")
        return redirect('home')

def add_record(request):
    form =AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Successfully Added!...")
                return redirect("home")
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "OOPS! You must be logged in..")
        return redirect("home")
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_form = Record.objects.get(id=pk)
        form =AddRecordForm(request.POST or None, instance=current_form)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Record have been updated")
            return redirect("home")
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "OOPS! You must be logged in..")
        return redirect("home")
