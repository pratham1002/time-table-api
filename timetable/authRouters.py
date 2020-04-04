from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.postgres.search import *
from .models import Student, Day, Hour
from .forms import loginForm, signUpForm

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)

        if form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                auth.login(request,user)
                return redirect('/home')
            else:
                return redirect('/login')
        
        else:
            return redirect('/login')

    form = loginForm()
    context = {
        "form": form
    }
    return render(request, 'login.html', context)

def signUp(request):
    if request.method == 'POST':
        form = signUpForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
            user.save()

            newstudent=Student(bits_id=request.POST['username'], email=request.POST['email'])
            newstudent.save()
            for i in range (0,6):
                newday = Day(day_number=i, student=newstudent)
                newday.save()
                for j in range (1,10):
                    newhour = Hour(day_number=i, hour_number=j, day=newday)
                    newhour.save()

            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])

            if user is not None:
                auth.login(request,user)
                return redirect('/home')

    form = signUpForm()
    context = {
        "form": form
    }
    return render(request, 'signUp.html', context)
        
def logout(request):
    auth.logout(request)
    return redirect('/')

def home(request):
    current_user=request.user
    userdata=Student.objects.get(email=current_user.email)
    userdays=Day.objects.filter(student=userdata.id)
    
    i=0
    userhours=Hour.objects.none()

    for day in userdays:
        userhours = userhours | Hour.objects.filter(day=day.id).order_by('id')

    context = {
        "userhours":userhours
    }

    return render(request, 'home.html', context)
