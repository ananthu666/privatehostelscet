from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.db.models import Sum, F, Case, When, Value, CharField
from django.http import JsonResponse
from django.utils import timezone
from .models import Hostel, Grievance, Vacancy, HostelRequest
import json
from decimal import Decimal
from datetime import time


def home(request):
    """Home page view"""
    return render(request, 'index.html')


def hostel(request):
    """Display approved hostels to the public"""
    # Only show approved hostels to the public
    approved_hostels = Hostel.objects.filter(approval_hostel_status='Approved')

    # Convert to list and format data
    hostel_list = list(approved_hostels.values())
    
    for entry in hostel_list:
        entry['average_rent'] = float(entry['average_rent'])
        # Handle null curfew (no curfew)
        if entry['curfew']:
            entry['curfew'] = entry['curfew'].strftime('%H:%M')
        else:
            entry['curfew'] = 'No Curfew'

    return render(request, 'hostel.html', {'my_list': hostel_list})


def page_admin(request):
    """Admin login page"""
    return render(request, 'login.html')


def login_page(request):
    """Handle admin login"""
    if request.method == "POST":
        username = request.POST.get('reg_username')
        password = request.POST.get('reg_pwd')
        print(f"Login attempt for username: {username}")
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/administration')
        else:
            # Add error message for failed login
            context = {'error': 'Invalid username or password'}
            return render(request, 'login.html', context)
    
    # Render login template for GET requests
    return render(request, 'login.html')


def grievance(request):
    """Display grievance form"""
    return render(request, 'grievance.html')


def commit_complaint(request):
    """Handle grievance complaint submission"""
    if request.method == "POST":
        try:
            # Extract form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            semester = request.POST.get('semester')
            department = request.POST.get('department')
            hostel = request.POST.get('hostel')
            location = request.POST.get('location')
            complaint = request.POST.get('complaint')

            # Validate that the hostel exists
            hostel_exists = Hostel.objects.filter(name__iexact=hostel).exists()
            if not hostel_exists:
                # Return error if hostel doesn't exist
                return render(request, 'grievance.html', {
                    'error': f'Hostel "{hostel}" does not exist. Please select from available hostels.',
                    'form_data': {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'semester': semester,
                        'department': department,
                        'location': location,
                        'complaint': complaint
                    }
                })

            # Create and save grievance
            Grievance.objects.create(
                full_name=name,
                email=email,
                phone=phone,
                semester=semester,
                department=department,
                hostel=hostel,
                location=location,
                complaint_text=complaint
            )
            print(f"Grievance submitted by: {name}")
            
            # Return success message
            return render(request, 'grievance.html', {
                'success': 'Your grievance has been submitted successfully! We will review and respond soon.'
            })
            
        except Exception as e:
            print(f"Error saving grievance: {str(e)}")
            return render(request, 'grievance.html', {
                'error': 'An error occurred while submitting your grievance. Please try again.'
            })
    
    return redirect('/grievance')


@login_required
def administration(request):
    """Admin dashboard with statistics and pending grievances"""
    # Get recent pending grievances
    recent_grievances = Grievance.objects.filter(
        complaint_status='Pending'
    ).order_by('-complaint_date', '-complaint_status')[:10]
    
    # Calculate statistics
    total_hostels = Hostel.objects.all().count()
    pending_grievances = Grievance.objects.filter(complaint_status='Pending').count()
    resolved_grievances = Grievance.objects.filter(complaint_status='Resolved').count()
    total_vacancy = Hostel.objects.aggregate(Sum('current_vacancy'))['current_vacancy__sum']
    pending_hostel_requests = HostelRequest.objects.filter(approval_status='Pending').count()
    
    if total_vacancy is None:
        total_vacancy = 0
    
    # Prepare statistics for template
    statistics = {
        'numberofhostel': total_hostels,
        'numberofpending_grievances': pending_grievances,
        'numberofresolved_grievances': resolved_grievances,
        'numberofvacancy': total_vacancy,
        'pending_hostel_requests': pending_hostel_requests
    }
    
    # Prepare grievance list for template
    grievance_list = [
        {
            'full_name': grievance.full_name,
            'complaint_text': grievance.complaint_text,
            'complaint_status': grievance.complaint_status
        }
        for grievance in recent_grievances
    ]
    
    return render(request, 'administration.html', {
        'my_list': grievance_list,
        'downbar': statistics
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_room_requests(request):
    """Handle room requests (placeholder function)"""
    # TODO: Define RoomRequest model or remove this function
    requests = []  # RoomRequest.objects.filter(approved=False)
    return render(request, 'administration.html', {'requests': requests})


@login_required
def insert_hostel(request):
    """Admin function to insert hostel directly"""
    if request.method == "POST":
        try:
            # Extract form data
            hostel_name = request.POST.get('hostelName')
            address = request.POST.get('address')
            owner_name = request.POST.get('ownerName')
            contact = request.POST.get('contact')
            capacity = request.POST.get('capacity')
            vacancy = request.POST.get('vacancy')
            gender = request.POST.get('gender')
            
            # Map form gender values to database values
            gender_mapping = {
                'mens': 'Men',
                'ladies': 'Women', 
                'mixed': 'Mixed',
                # Also handle if the form already sends correct values
                'Men': 'Men',
                'Women': 'Women',
                'Mixed': 'Mixed'
            }
            mapped_gender = gender_mapping.get(gender, 'Mixed')  # Default to Mixed if unknown
            rent = request.POST.get('rent')
            acc_type = request.POST.get('type')
            curfew_type = request.POST.get('curfewType', 'time')
            curfew_raw = request.POST.get('curfewTime', '').strip()
            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')
            mess = request.POST.get('mess')
            distance = request.POST.get('distance')
            
            # Handle curfew time based on type selection
            if curfew_type == 'none':
                curfew = None
            else:
                # Handle empty curfew time - set default to 22:00 (10 PM)
                curfew = curfew_raw if curfew_raw else '22:00'
            
            # Create hostel
            Hostel.objects.create(
                name=hostel_name,
                address=address,
                owner_name=owner_name,
                contact_details=contact,
                total_capacity=capacity,
                current_vacancy=vacancy,
                mens_or_ladies=mapped_gender,
                average_rent=rent,
                accommodation_type=acc_type,
                curfew=curfew,
                longitude=longitude,
                latitude=latitude,
                mess=mess,
                distance=distance
            )
            print(f"Hostel '{hostel_name}' inserted successfully")
            
        except Exception as e:
            print(f"Error inserting hostel: {str(e)}")
    
    return redirect('/administration')


def admin_logout(request):
    """Handle admin logout"""
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
        vacancycount = int(request.POST['vacancycount'])
        hostel_id = request.POST.get('hostel_id', '')
        
        print(f"Request room - Hostel: {hostelname}, Vacancy: {vacancycount}, ID: {hostel_id}")
        
        # First check by ID if provided, then by name
        hostel = None
        if hostel_id:
            try:
                hostel = Hostel.objects.get(id=hostel_id)
            except Hostel.DoesNotExist:
                pass
        
        if not hostel:
            try:
                hostel = Hostel.objects.get(name=hostelname)
            except Hostel.DoesNotExist:
                pass
        
        if hostel:
            # Validate vacancy change (supports both positive and negative values)
            new_total_vacancy = hostel.current_vacancy + vacancycount
            
            # Check if new vacancy would be negative (trying to remove more than available)
            if new_total_vacancy < 0:
                max_reduction = hostel.current_vacancy
                error_msg = f'Cannot reduce vacancy by {abs(vacancycount)}. Current vacancy is only {hostel.current_vacancy}. Maximum reduction: {max_reduction}'
                return render(request, 'request_room.html', {
                    'error_message': error_msg,
                    'hostel_name': hostelname,
                    'vacancy_count': vacancycount
                })
            
            # Check if new vacancy would exceed total capacity (when adding)
            if new_total_vacancy > hostel.total_capacity:
                available_to_add = hostel.total_capacity - hostel.current_vacancy
                error_msg = f'Cannot add {vacancycount} vacancy. Current vacancy: {hostel.current_vacancy}, Total capacity: {hostel.total_capacity}. You can only add up to {available_to_add} more vacancy slots.'
                return render(request, 'request_room.html', {
                    'error_message': error_msg,
                    'hostel_name': hostelname,
                    'vacancy_count': vacancycount
                })
            
            # Create vacancy request with proper hostel relationship
            ins = Vacancy(
                hostel=hostel,
                hostelname=hostelname, 
                vacancycount=vacancycount
            )
            ins.save()
            print(f"Vacancy request saved for hostel: {hostelname} (ID: {hostel.id})")
            return render(request, "vaccancysucc.html", {
                'hostel_name': hostelname,
                'vacancy_count': vacancycount,
                'current_vacancy': hostel.current_vacancy,
                'total_capacity': hostel.total_capacity
            })
        else:
            print(f"Hostel not found: {hostelname}")
            return render(request, 'request_room.html', {
                'error_message': f'Hostel "{hostelname}" does not exist in our database. Please check the name and try again.',
                'hostel_name': hostelname,
                'vacancy_count': vacancycount
            })
    
    return render(request, 'request_room.html')

def approve_vacancy(request):
    """Handle vacancy approval/rejection by admin"""
    if request.method == 'POST':
        vacancy_id = request.POST.get('vacancy_id')
        action = request.POST.get('action', 'approve')
        
        try:
            vacancy_request = Vacancy.objects.get(id=vacancy_id)
            
            if action == 'approve':
                # Get the related hostel
                hostel = None
                if vacancy_request.hostel:
                    hostel = vacancy_request.hostel
                else:
                    # Fallback to name lookup if hostel relationship is missing
                    try:
                        hostel = Hostel.objects.get(name=vacancy_request.hostelname)
                        # Update the vacancy request to link to the hostel
                        vacancy_request.hostel = hostel
                    except Hostel.DoesNotExist:
                        print(f"Hostel '{vacancy_request.hostelname}' not found")
                        # Could redirect with error message
                
                if hostel:
                    # Handle both positive and negative vacancy changes
                    current_vacancy = hostel.current_vacancy or 0
                    vacancy_change = vacancy_request.vacancycount
                    new_vacancy_count = current_vacancy + vacancy_change
                    
                    # Validate the change before applying
                    if new_vacancy_count < 0:
                        print(f"Cannot approve vacancy request: Would result in negative vacancy ({new_vacancy_count})")
                        # You could add error handling here
                        return redirect('/vaccancy')  # Redirect back with error
                    
                    if new_vacancy_count > hostel.total_capacity:
                        print(f"Cannot approve vacancy request: Would exceed total capacity ({new_vacancy_count} > {hostel.total_capacity})")
                        # You could add error handling here
                        return redirect('/vaccancy')  # Redirect back with error
                    
                    # Apply the change
                    hostel.current_vacancy = new_vacancy_count
                    hostel.save()
                    
                    # Mark the vacancy request as approved
                    vacancy_request.approved = True
                    vacancy_request.save()
                    
                    change_type = "Added" if vacancy_change > 0 else "Removed"
                    abs_change = abs(vacancy_change)
                    print(f"Approved vacancy for {hostel.name}: {change_type} {abs_change} rooms. Total vacancy: {new_vacancy_count}")
                
                
            elif action == 'reject':
                # Simply delete the vacancy request for rejection
                vacancy_request.delete()
                print(f"Rejected and deleted vacancy request for {vacancy_request.hostelname}")
                
        except Vacancy.DoesNotExist:
            print(f"Vacancy request with ID {vacancy_id} not found")
        except Exception as e:
            print(f"Error processing vacancy request: {str(e)}")
    
    # Fetch all pending vacancy requests to show on the approval page
    pending_vacancies = Vacancy.objects.filter(approved=False).order_by('-created_at')
    return render(request, 'vaccancy.html', {'vacancies': pending_vacancies})


def hostel_reg(request):
    """Display hostel registration form"""
    return render(request, 'hostel_reg.html')

def commit_hostel_reg(request):
    context = {'success': False}
    if request.method == "POST":
        try:
            hostelname = request.POST['hostelName']
            address = request.POST['address']
            ownername = request.POST['ownerName']
            contact = request.POST['contact']
            
            # Get capacity and vacancy values for validation
            total_capacity = int(request.POST.get('capacity', 0))
            vacancy = int(request.POST.get('vacancy', 0))
            
            # Validate that vacancy doesn't exceed capacity
            if vacancy > total_capacity:
                context = {
                    'success': False, 
                    'error': f'Current vacancy ({vacancy}) cannot be greater than total capacity ({total_capacity}). Please check your values.'
                }
                return render(request, 'hostel_reg.html', context)
            
            gender = request.POST['gender']
            
            # Map form gender values to database values
            gender_mapping = {
                'mens': 'Men',
                'ladies': 'Women', 
                'mixed': 'Mixed',
                # Also handle if the form already sends correct values
                'Men': 'Men',
                'Women': 'Women',
                'Mixed': 'Mixed'
            }
            mapped_gender = gender_mapping.get(gender, 'Mixed')  # Default to Mixed if unknown
            rent = request.POST['rent']
            acc_type = request.POST['type']
            curfew_type = request.POST.get('curfewType', 'time')
            curfew_raw = request.POST.get('curfewTime', '')
            longitude = request.POST['longitude']
            latitude = request.POST['latitude']
            mess = request.POST['mess']
            distance = request.POST['distance']
            
            # Debug: Print the raw curfew value
            print(f"Raw curfew value: '{curfew_raw}' (type: {type(curfew_raw)})")
            print(f"Curfew type: '{curfew_type}'")
            
            # Handle curfew time based on type selection
            if curfew_type == 'none':
                curfew = None
                print("Setting curfew to None (no curfew)")
            else:
                # Handle empty curfew time - set default to 22:00 (10 PM)
                if not curfew_raw or curfew_raw.strip() == '' or curfew_raw is None:
                    curfew = '22:00'
                    print(f"Setting default curfew: {curfew}")
                else:
                    curfew = curfew_raw.strip()
                    print(f"Using provided curfew: {curfew}")
                
                # Validate time format before saving (only if not None)
                from datetime import time as datetime_time
                try:
                    # Test if the time string is valid
                    datetime_time.fromisoformat(curfew)
                    print(f"Time validation successful for: {curfew}")
                except ValueError:
                    print(f"Invalid time format: {curfew}, using default")
                    curfew = '22:00'
            
            print(f"Final curfew value before saving: '{curfew}'")
            
            Hostel(name=hostelname, address=address,
                   owner_name=ownername, contact_details=contact,
                   total_capacity=total_capacity, current_vacancy=vacancy, 
                   mens_or_ladies=mapped_gender, average_rent=rent,
                   accommodation_type=acc_type, curfew=curfew, longitude=longitude,
                   latitude=latitude, mess=mess, distance=distance).save()
            context = {'success': True}
            
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            context = {'success': False, 'error': str(e)}

        return render(request, 'hostel_reg.html', context)
    
    return render(request, 'hostel_reg.html', context)

def hostel_approval(request):
    approvals_list = Hostel.objects.all()
    approvals = list(approvals_list.values())
    # print(approvals)

    for entry in approvals:
        if entry['curfew'] is not None:
            entry['curfew'] = entry['curfew'].strftime('%H:%M')
        else:
            entry['curfew'] = 'Not specified'
      
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

def search_hostels_api(request):
    """API endpoint to search hostels by name for vacancy form"""
    if request.method == 'GET':
        query = request.GET.get('q', '').strip()
        
        if len(query) < 2:  # Only search if query is at least 2 characters
            return JsonResponse({
                'hostels': [],
                'message': 'Type at least 2 characters to search'
            })
        
        # Search hostels by name (case-insensitive)
        hostels = Hostel.objects.filter(
            name__icontains=query
        ).values('id', 'name', 'address', 'owner_name', 'current_vacancy', 'total_capacity')[:10]  # Limit to 10 results
        
        hostel_list = list(hostels)
        
        if not hostel_list:
            return JsonResponse({
                'hostels': [],
                'message': f'No hostels found matching "{query}"'
            })
        
        return JsonResponse({
            'hostels': hostel_list,
            'message': f'Found {len(hostel_list)} hostel(s)'
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def hostel_registration(request):
    """Display hostel registration form for new hostel owners"""
    return render(request, 'hostel_registration.html')


def submit_hostel_request(request):
    """Handle hostel registration request submission"""
    if request.method == 'POST':
        try:
            # Get capacity and vacancy values for validation
            total_capacity = int(request.POST.get('capacity', 0))
            current_vacancy = int(request.POST.get('vacancy', 0))
            
            # Validate that vacancy doesn't exceed capacity
            if current_vacancy > total_capacity:
                error_msg = f'Current vacancy ({current_vacancy}) cannot be greater than total capacity ({total_capacity}). Please check your values.'
                return render(request, 'hostel_registration.html', {
                    'error': error_msg,
                    'form_data': request.POST  # Keep form data to avoid user re-entering everything
                })
            
            # Parse curfew time
            curfew_type = request.POST.get('curfewType', 'time')
            curfew_str = request.POST.get('curfewTime', '22:00')
            
            if curfew_type == 'none':
                curfew_time = None
            else:
                try:
                    curfew_time = time.fromisoformat(curfew_str)
                except ValueError:
                    curfew_time = time(22, 0)  # Default to 10 PM
            
            # Map form gender values to database values
            gender_form_value = request.POST.get('gender', 'mixed')
            gender_mapping = {
                'mens': 'Men',
                'ladies': 'Women', 
                'mixed': 'Mixed',
                # Also handle if the form already sends correct values
                'Men': 'Men',
                'Women': 'Women',
                'Mixed': 'Mixed'
            }
            mapped_gender = gender_mapping.get(gender_form_value, 'Mixed')
            
            # Create hostel request
            hostel_request = HostelRequest.objects.create(
                name=request.POST.get('hostelName', ''),
                address=request.POST.get('address', ''),
                owner_name=request.POST.get('ownerName', ''),
                contact_details=request.POST.get('contact', ''),
                total_capacity=total_capacity,
                current_vacancy=current_vacancy,
                mens_or_ladies=mapped_gender,
                average_rent=int(request.POST.get('rent', 0)),
                accommodation_type=request.POST.get('type', 'hostel'),
                curfew=curfew_time,
                longitude=float(request.POST.get('longitude', 0.0)),
                latitude=float(request.POST.get('latitude', 0.0)),
                distance=float(request.POST.get('distance', 0.0)),
                mess=request.POST.get('mess', 'No'),
            )
            
            print(f"New hostel request submitted: {hostel_request.name} by {hostel_request.owner_name}")
            return render(request, 'hostel_registration_success.html', {
                'hostel_name': hostel_request.name,
                'owner_name': hostel_request.owner_name
            })
            
        except ValueError as e:
            print(f"Error in hostel request submission: {str(e)}")
            return render(request, 'hostel_registration.html', {
                'error': 'Please check your input values and try again. Make sure all numeric fields contain valid numbers.',
                'form_data': request.POST
            })
        except Exception as e:
            print(f"Unexpected error in hostel request: {str(e)}")
            return render(request, 'hostel_registration.html', {
                'error': 'An error occurred. Please try again.',
                'form_data': request.POST
            })
    
    return redirect('/hostel_registration')


@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_hostel_requests(request):
    """Handle hostel request approval/rejection by admin"""
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        request_type = request.POST.get('request_type')
        action = request.POST.get('action', 'approve')
        admin_notes = request.POST.get('admin_notes', '')
        
        try:
            if request_type == 'new_registration':
                # Handle HostelRequest approval/rejection
                hostel_request = HostelRequest.objects.get(id=request_id)
                
                if action == 'approve':
                    # Create a new Hostel record from the request
                    new_hostel = Hostel.objects.create(
                        name=hostel_request.name,
                        address=hostel_request.address,
                        owner_name=hostel_request.owner_name,
                        contact_details=hostel_request.contact_details,
                        total_capacity=hostel_request.total_capacity,
                        current_vacancy=hostel_request.current_vacancy,
                        mens_or_ladies=hostel_request.mens_or_ladies,
                        average_rent=hostel_request.average_rent,
                        accommodation_type=hostel_request.accommodation_type,
                        curfew=hostel_request.curfew,
                        longitude=hostel_request.longitude,
                        latitude=hostel_request.latitude,
                        distance=hostel_request.distance,
                        mess=hostel_request.mess,
                        approval_hostel_status='Approved'
                    )
                    
                    # Update the request status
                    hostel_request.approval_status = 'Approved'
                    hostel_request.approved_at = timezone.now()
                    hostel_request.admin_notes = admin_notes
                    hostel_request.save()
                    
                    print(f"Approved hostel request: {hostel_request.name}. Created hostel ID: {new_hostel.id}")
                    
                elif action == 'reject':
                    hostel_request.approval_status = 'Rejected'
                    hostel_request.admin_notes = admin_notes
                    hostel_request.save()
                    print(f"Rejected hostel request: {hostel_request.name}")
                    
            elif request_type == 'existing_hostel':
                # Handle existing Hostel approval/rejection
                hostel = Hostel.objects.get(id=request_id)
                
                if action == 'approve':
                    hostel.approval_hostel_status = 'Approved'
                    hostel.save()
                    print(f"Approved existing hostel: {hostel.name}")
                    
                elif action == 'reject':
                    hostel.approval_hostel_status = 'Rejected'
                    hostel.save()
                    print(f"Rejected existing hostel: {hostel.name}")
                    
        except (HostelRequest.DoesNotExist, Hostel.DoesNotExist):
            print(f"Request with ID {request_id} not found")
        except Exception as e:
            print(f"Error processing request: {str(e)}")
    
    # Fetch both HostelRequest objects and pending Hostel objects
    hostel_requests = HostelRequest.objects.all().order_by('-created_at')
    pending_hostels = Hostel.objects.filter(approval_hostel_status='Pending').order_by('-id')
    
    # Convert pending hostels to a similar format as hostel requests for the template
    combined_requests = []
    
    # Add HostelRequest objects
    for req in hostel_requests:
        combined_requests.append({
            'id': req.id,
            'name': req.name,
            'owner_name': req.owner_name,
            'contact_details': req.contact_details,
            'address': req.address,
            'total_capacity': req.total_capacity,
            'current_vacancy': req.current_vacancy,
            'mens_or_ladies': req.mens_or_ladies,
            'average_rent': req.average_rent,
            'accommodation_type': req.accommodation_type,
            'mess': req.mess,
            'curfew': req.curfew,
            'distance': req.distance,
            'latitude': req.latitude,
            'longitude': req.longitude,
            'approval_status': req.approval_status,
            'created_at': req.created_at,
            'approved_at': req.approved_at,
            'admin_notes': req.admin_notes,
            'request_type': 'new_registration'
        })
    
    # Add pending Hostel objects
    for hostel in pending_hostels:
        combined_requests.append({
            'id': hostel.id,
            'name': hostel.name,
            'owner_name': hostel.owner_name,
            'contact_details': hostel.contact_details,
            'address': hostel.address,
            'total_capacity': hostel.total_capacity,
            'current_vacancy': hostel.current_vacancy,
            'mens_or_ladies': hostel.mens_or_ladies,
            'average_rent': hostel.average_rent,
            'accommodation_type': hostel.accommodation_type,
            'mess': hostel.mess,
            'curfew': hostel.curfew,
            'distance': hostel.distance,
            'latitude': hostel.latitude,
            'longitude': hostel.longitude,
            'approval_status': 'Pending',  # Map hostel status to request status
            'created_at': None,  # Hostels don't have created_at
            'approved_at': None,
            'admin_notes': '',
            'request_type': 'existing_hostel'
        })
    
    # Sort combined list by creation date (None values last)
    combined_requests.sort(key=lambda x: x['created_at'] or timezone.now(), reverse=True)
    
    return render(request, 'hostel_requests.html', {'requests': combined_requests})