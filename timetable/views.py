import xlrd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.postgres.search import *
from django.core.exceptions import *
from .models import Student,Day,Hour
import  enum

def ConvertToIntegerList(strlist):
    intlist=[]
    for ele in strlist:
        if ele == 'M':
            intlist.append(0)
        if ele == 'T':
            intlist.append(1)
        if ele == 'W':
            intlist.append(2)
        if ele == 'Th':
            intlist.append(3)
        if ele == 'F':
            intlist.append(4)
        if ele == 'S':
            intlist.append(5)
    return(intlist)
    
def Home(request):
    current_user=request.user
    userdata=Student.objects.get(email=current_user.email)
    userdays=Day.objects.filter(student=userdata.id)
    
    i=0
    userhours=Hour.objects.none()

    for day in userdays:
        userhours = userhours | Hour.objects.filter(day=day.id).order_by('id')

    return render(request, 'Home.html', {"userhours":userhours})

def index(request):
    return render(request, 'index.html')

def Login(request):
    return render(request, 'Login.html')

def SignUp(request):
    return render(request,'SignUp.html')

def LoginUser(request):
    username=request.POST['username']
    password=request.POST['password']

    user=auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        return Home(request)

    else:

        return render(request,'Login.html',{"message":"invalid password"})

def CreateUser(request):
    username=request.POST['username']
    email=request.POST['email']
    password1=request.POST['password1']
    password2=request.POST['password2']

    if(password1==password2):
        if User.objects.filter(email=email).exists():
            return render(request,'SignUp.html',{"message":"User already exists"})
        else:
            user=User.objects.create_user(username=username, password=password1, email=email)
            user.save()

            newstudent=Student(bits_id=username, email=email)
            newstudent.save()
            for i in range (0,6):
                newday=Day(day_number=i, student=newstudent)
                newday.save()
                for j in range (1,10):
                    newhour=Hour(day_number=i, hour_number=j, day=newday)
                    newhour.save()

            user=auth.authenticate(username=username,password=password1)

            if user is not None:
                auth.login(request,user)
                return Home(request)
            
    else:
        return render(request,'SignUp.html',{"message":"Passwords Do Not Match"})

def CourseData(request):

    course_number=request.GET['course_number']

    current_user=request.user
    userdata=Student.objects.get(email=current_user.email)
    userdays=Day.objects.filter(student=userdata.id)
    
    userhours=Hour.objects.none()

    for day in userdays:
        userhours = userhours | Hour.objects.filter(day=day.id).order_by('id')

    loc=("Timetable.xlsx")
    wb=xlrd.open_workbook(loc)
    sheet=wb.sheet_by_index(0)

    lectures=[]
    practicals=[]
    tutorials=[]
    section_number=0
    instructors=[]
    row_number=0

    for i in range(sheet.nrows):

        if sheet.cell_value(i,1) == course_number :
            
            for j in range(sheet.nrows):

                if j == 0:
                    row_number= i
                    instructors.append(sheet.cell_value(i+j,9))
                    try:
                        instructors.append(int(sheet.cell_value(i+j,10)))
                    except :
                        instructors.append(sheet.cell_value(i+j,10))
                    instructors.append(sheet.cell_value(i+j,7))
                    section_number = section_number + 1
                    continue

                elif len(str(sheet.cell_value(i+j,1))):
                    lectures.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )
                    break

                elif len(str(sheet.cell_value(i+j,2))):
                    lectures.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )

                    instructors=[]
                    section_number=0

                    if sheet.cell_value(i+j,2) == "Tutorial":

                        for k in range(sheet.nrows):
                            if k == 0:
                                row_number=i+j+k
                                instructors.append(sheet.cell_value(i+j+k,9))
                                try:
                                    instructors.append(int(sheet.cell_value(i+j+k,10)))
                                except :
                                    instructors.append(sheet.cell_value(i+j+k,10))
                                instructors.append(sheet.cell_value(i+j+k,7))
                                section_number = section_number + 1
                                continue

                            elif len(str(sheet.cell_value(i+j+k,1))):
                                tutorials.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )
                                break

                            elif len(str(sheet.cell_value(i+j+k,6))):
                                tutorials.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )
                                instructors=[]
                                section_number = section_number + 1
                                row_number=i+j+k
                                instructors.append(sheet.cell_value(i+j+k,9))
                                try:
                                    instructors.append(int(sheet.cell_value(i+j+k,10)))
                                except:
                                    instructors.append(sheet.cell_value(i+j+k,10))
                                instructors.append(sheet.cell_value(i+j+k,7))

                            else:
                                instructors.append(sheet.cell_value(i+j+k,7))
                        break

                    if sheet.cell_value(i+j,2) == "Practical":

                        for k in range(sheet.nrows):
                            if k == 0:
                                row_number=i+j+k
                                instructors.append(sheet.cell_value(i+j+k,9))
                                try:
                                    instructors.append(int(sheet.cell_value(i+j+k,10)))
                                except :
                                    instructors.append(sheet.cell_value(i+j+k,10))
                                instructors.append(sheet.cell_value(i+j+k,7))
                                section_number = section_number + 1
                                continue

                            elif len(str(sheet.cell_value(i+j+k,1))):
                                practicals.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )
                                break

                            elif len(str(sheet.cell_value(i+j+k,6))):
                                practicals.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )
                                instructors=[]
                                section_number = section_number + 1
                                row_number=i+j+k
                                instructors.append(sheet.cell_value(i+j+k,9))
                                try:
                                    instructors.append(int(sheet.cell_value(i+j+k,10)))
                                except: 
                                    instructors.append(sheet.cell_value(i+j+k,10))
                                instructors.append(sheet.cell_value(i+j+k,7))

                            else:
                                instructors.append(sheet.cell_value(i+j+k,7))
                        break

                elif len(str(sheet.cell_value(i+j,6))):
                    lectures.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )
                    instructors=[]
                    section_number = section_number + 1
                    row_number=i+j
                    instructors.append(sheet.cell_value(i+j,9))
                    try:
                        instructors.append(int(sheet.cell_value(i+j,10)))
                    except :
                        instructors.append(sheet.cell_value(i+j,10))
                    instructors.append(sheet.cell_value(i+j,7))

                
                else:
                    instructors.append(sheet.cell_value(i+j,7))

            break
    if len(lectures) == 0:
        return render(request, 'Home.html', {"message":"Invalid Course Name"})

    return render(request, 'Home.html', {"course_number":course_number, "lectures": lectures, "practicals": practicals, "tutorials": tutorials, "userhours":userhours})

def AddSlot(request):

    slot=request.POST['slot']
    course_number=request.POST['course_number']
    slotdata=slot.split(', ')

    current_user=request.user
    userdata=Student.objects.get(email=current_user.email)
    userdays=Day.objects.filter(student=userdata.id)
    
    userhours=Hour.objects.none()

    for day in userdays:
        userhours = userhours | Hour.objects.filter(day=day.id).order_by('id')

    section_number=slotdata[0]
    days=slotdata[1].split()
    hours=slotdata[2].split()
    days=ConvertToIntegerList(days)


    #print(days)
    #print(hours)
    
    for day in days:
        for hour in hours:
            for userhour in userhours:
                if userhour.day_number==day and userhour.hour_number==int(hour) :
                    if userhour.status==False:
                        #print("change done")
                        userhour.course=course_number
                        userhour.status=True
                        userhour.save()
                    else:
                        return render(request, 'Home.html',{"userhours":userhours})
        
    return Home(request)

def RemoveCourse(request):
    course_number=request.GET['course_number']
    current_user=request.user
    userdata=Student.objects.get(email=current_user.email)
    userdays=Day.objects.filter(student=userdata.id)
    
    userhours=Hour.objects.none()

    for day in userdays:
        userhours = userhours | Hour.objects.filter(day=day.id).order_by('id')


    for userhour in userhours:
        if userhour.course==course_number :
            userhour.status=False
            userhour.course=''
            userhour.save()

    return Home(request)

def Logout(request):
    auth.logout(request)
    return redirect('/')

def clear(request):
    current_user=request.user
    userdata=Student.objects.get(email=current_user.email)
    userdays=Day.objects.filter(student=userdata.id)
    
    userhours=Hour.objects.none()

    for day in userdays:
        userhours = userhours | Hour.objects.filter(day=day.id).order_by('id')
        for userhour in userhours:
            userhour.status=False
            userhour.course=''
            userhour.save()

    return render(request, 'Home.html',{"userhours":userhours})
