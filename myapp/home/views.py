from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from .models import Hostel, Grievance,Vacancy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
import json
from decimal import Decimal
from datetime import time
from django.db.models import Sum,F, Case, When, Value, CharField




def home(request):

    return render(request, 'index.html')


def hostel(request):
    my_list1 = Hostel.objects.all()

    my_list = list(my_list1.values())
    
    for entry in my_list:
        
        entry['average_rent'] = float(entry['average_rent'])
        entry['curfew'] = entry['curfew'].strftime('%H:%M')

# Convert the list to JSON
    # json_data = json.dumps(my_list)
    # print(my_list)

    return render(request, 'hostel.html', {'my_list': my_list})

#def vaccancy(request):
    if request.method=="POST":
        name=request.POST['hostelName']
        availableRooms=request.POST['availableRooms']
        ins=Vaccancy(name=name,availableRooms=availableRooms)
        ins.save()
        if name and availableRooms:
            hostel = get_object_or_404(Hostel, id=hostel_id)
            # Create a new vacancy request
            Vaccancy.objects.create(
                hostel=hostel,
                availableRooms=availableRooms
            )
            return redirect('request_vacancy_approval')  # Redirect to the admin page
        else:
            return HttpResponse("Invalid data submitted.", status=400)
    else:
        return render(request, 'vaccancy.html')
    
def page_admin(request):

    return render(request, 'login.html')


def login_page(request):
    if request.method == "POST":

        username = request.POST['reg_username']
        password = request.POST['reg_pwd']
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('/administration')

        else:
            return redirect('/login')
    return HttpResponse("you are not admin")


def grievance(request):
    return render(request, 'grievance.html')


def commit_complaint(request):

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        semester = request.POST['semester']
        department = request.POST['department']
        hostel = request.POST['hostel']
        location = request.POST['location']
        complaint = request.POST['complaint']

        Grievance(full_name=name, email=email, phone=phone,
                  semester=semester, department=department, hostel=hostel,
                  location=location, complaint_text=complaint).save()
    return redirect('/grievance')


@login_required
def administration(request):
    my_list1 = Grievance.objects.filter(complaint_status='Pending').order_by(
        '-complaint_date', '-complaint_status')[:10]
    numberofhostel = Hostel.objects.all().count()
    numberofpending_grievances = Grievance.objects.filter(
        complaint_status='Pending').count()
    numberofresolved_grievances = Grievance.objects.filter(
        complaint_status='Resolved').count()
    numberofvacancy = Hostel.objects.aggregate(Sum('current_vacancy'))[
        'current_vacancy__sum']

    if numberofvacancy is None:
        numberofvacancy = 0
    downbar = {
        'numberofhostel': numberofhostel,
        'numberofpending_grievances': numberofpending_grievances,
        'numberofresolved_grievances': numberofresolved_grievances,
        'numberofvacancy': numberofvacancy
    }
# Create a list of dictionaries
    my_list = [
        {
            'full_name': grievance.full_name,
            'complaint_text': grievance.complaint_text,
            'complaint_status': grievance.complaint_status
        }
        for grievance in my_list1
    ]
    return render(request, 'administration.html', {'my_list': my_list, 'downbar': downbar})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_room_requests(request):
    requests = RoomRequest.objects.filter(approved=False)
    return render(request, 'administration.html', {'requests': requests})

def insert_hostel(request):
    if request.method == "POST":
        print("hi")
        print("Please")
        # name = request.POST['name']
        hostelname = request.POST['hostelName']
        address = request.POST['address']
        ownername = request.POST['ownerName']
        contact = request.POST['contact']
        capacity = request.POST['capacity']
        vacancy = request.POST['vacancy']
        gender = request.POST['gender']
        rent = request.POST['rent']
        acc_type = request.POST['type']
        curfew = request.POST['curfewTime']
        longitude = request.POST['longitude']
        latitude = request.POST['latitude']
        mess = request.POST['mess']
        distance = request.POST['distance']
        print(hostelname, address, ownername, contact, capacity, vacancy,
              gender, rent, acc_type, curfew, longitude, mess, distance)
        Hostel(name=hostelname, address=address,
               owner_name=ownername, contact_details=contact,
               total_capacity=capacity, current_vacancy=vacancy,
               mens_or_ladies=gender, average_rent=rent,
               accommodation_type=acc_type, curfew=curfew, longitude=longitude,
               latitude=latitude, mess=mess, distance=distance).save()
    return redirect('/administration')




def admin_logout(request):
    logout(request)
    return redirect('/')


def admin_complaint_view(request):
    my_list1 = Grievance.objects.all().order_by(
        Case(
            When(complaint_status='Pending', then=Value('A')),
            When(complaint_status='Resolved', then=Value('Z')),
            default=F('complaint_status'),
            output_field=CharField(),
        ),
        '-complaint_date'
    )[:10]
    my_list = list(my_list1.values())
    print(my_list)
    
    # 
    for entry in my_list:
        
        entry['complaint_time'] = entry['complaint_time'].strftime('%H:%M')
        entry['complaint_date'] = entry['complaint_date'].strftime('%d-%m-%Y')
    # print(my_list)
    return render(request, 'complaint_view.html', {'my_list': my_list})


def status_view(request,id):
    # Extract id parameter from the URL
    complaint_id = request.GET.get('id')
    # print(complaint_id)
    # toggle the status of the complaint
    complaint = Grievance.objects.get(id=complaint_id)
    if complaint.complaint_status == 'Pending':
        complaint.complaint_status = 'Resolved'
    else:
        complaint.complaint_status = 'Pending'
    complaint.save()
    return redirect('/admin_complaint_view')

def bulkadd(request):
    
    return HttpResponse("Bulk add page")


def request_room(request):
    if request.method == "POST":
        hostelname = request.POST['hostelname']
        vacancycount = request.POST['vacancycount']
        if Hostel.objects.filter(name=hostelname).exists():
            ins=Vacancy(hostelname=hostelname,vacancycount=vacancycount)
            ins.save()
            print("yes")
            return render(request,"vaccancysucc.html")
             
        else:
            return HttpResponse("Hostel Does Not Exist")
    return render(request, 'request_room.html')

def approve_vacancy(request):
    if request.method == 'POST':
        hostel_name = request.POST.get('hostelname')
        vacancy_count = request.POST.get('vacancycount')
        
        try:
            hostel = Hostel.objects.get(name=hostel_name)
            print(hostel)
            hostel.current_vacancy = int(vacancy_count)
            hostel.save()
            # Optionally, you could also mark the vacancy as approved or delete it
            Vacancy.objects.filter(hostelname=hostel_name).delete()
        except Hostel.DoesNotExist:
            pass  # Handle the case where the hostel does not exist

    # Fetch all vacancies to show on the approval page
    vacancies = Vacancy.objects.all()
    return render(request, 'vaccancy.html', {'vacancies': vacancies})






def hostel_reg(request):
    return render(request, 'hostel_reg.html')

def commit_hostel_reg(request):
    context = {'success' : False}
    if request.method == "POST":
        print("hi")
        print("Please")
        # name = request.POST['name']
        hostelname = request.POST['hostelName']
        address = request.POST['address']
        ownername = request.POST['ownerName']
        contact = request.POST['contact']
        
        vacancy = request.POST['vacancy']
        gender = request.POST['gender']
        rent = request.POST['rent']
        acc_type = request.POST['type']
        curfew = request.POST['curfewTime']
        longitude = request.POST['longitude']
        latitude = request.POST['latitude']
        mess = request.POST['mess']
        distance = request.POST['distance']
        # print(hostelname, address, ownername, contact, vacancy,
        #      gender, rent, acc_type, curfew, longitude, mess, distance)
        # try:
        Hostel(name=hostelname, address=address,
               owner_name=ownername, contact_details=contact,
               current_vacancy=vacancy,mens_or_ladies=gender, average_rent=rent,
               accommodation_type=acc_type, curfew=curfew, longitude=longitude,
               latitude=latitude, mess=mess, distance=distance).save()
        context = {'success' : True}

        return render(request, 'hostel_reg.html', context)

def hostel_approval(request):
    approvals_list = Hostel.objects.all()
    approvals = list(approvals_list.values())
    # print(approvals)

    for entry in approvals:
        entry['curfew'] = entry['curfew'].strftime('%H:%M')
      
    return render(request, 'hostel_approval.html', {'approvals': approvals})

def hostel_status_view(request,id):
    # Extract id parameter from the URL
    hostel_id = request.GET.get('id')
    # print(complaint_id)
    # toggle the status of the complaint
    hostel = Hostel.objects.get(id=hostel_id)
    if hostel.approval_hostel_status == 'Pending':
        hostel.approval_hostel_status = 'Approved'
    else:
        hostel.approval_hostel_status = 'Pending'
    hostel.save()
    return redirect('/hostel_approval')

# def hostel_notifications(request):
#     unapproved_hostels = [
#         {
#             'name': hostel.name,
#             'owner_name': hostel.owner_name,
#             'approval_hostel_status': hostel.approval_hostel_status
#         }
#         for hostel in Hostel.objects.filter(approval_hostel_status='pending')
#     ]
#     return render(request, 'administration.html', {'unapproved_hostels': unapproved_hostels})


