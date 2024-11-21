from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserDetail
from django.utils import timezone
from django.http import HttpResponse
from .models import Vehicle,Driver,Consignment
from django.db.models import Count
from datetime import datetime


# Create your views here.
def index(request):


    return render(request,'index.html') 


def login_register(request):
    return render(request,'login_register.html')

def customerlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check the role from the user's profile
            try:


                auth_id=User.objects.get(username=username).id

                auth_role=UserDetail.objects.get(auth_user_id=auth_id).role

                if auth_role == 'Admin':  # Assuming role is a related field in UserDetail model
                    return redirect('admindashboard')  # Redirect to admin dashboard
                else:
                    return redirect('customerdashboard')  # Redirect to customer dashboard
            except UserDetail.DoesNotExist:
                return redirect('index')  # Redirect if no user detail is found, can be modified
        else:
            return redirect('index')  # Redirect to login page or show an error message

    return render(request, 'customerlogin.html')

def customerregister(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        fname = request.POST['fname']  # Optional field
        lname = request.POST['lname']  # Optional field
        role = request.POST.get('role', 'Customer')  # Default role is 'Customer'
        user = User.objects.create_user(username=username, email=email, password=password)
        # Create the associated UserDetail object
        user.save()


        UserDetail.objects.create(
            auth_user=user,
            fname=fname,
            lname=lname,
            role=role,
            username=username,
            password=password
        )
        return redirect('customerlogin')  # Redirect to the login page after successful registration
    return render(request, 'customerlogin.html')

def customerdashboard(request):
    driver_count = Driver.objects.filter(created_by_id=request.user.id).count()
    vehicle_count = Vehicle.objects.filter(created_by_id=request.user.id).count()
    ongoing_consignment_count = Consignment.objects.filter(status='Pending').filter(created_by_id=request.user.id).count()
    approved_consignment_count = Consignment.objects.filter(status='Approved').filter(created_by_id=request.user.id).count()




    compact = {'driver_count':driver_count, 'vehicle_count':vehicle_count,'ongoing_consignment_count':ongoing_consignment_count,'approved_consignment_count':approved_consignment_count}
    return render(request, 'customerdashboard.html',compact)

def customlogout(request):
    # Log out the user
    logout(request)
    # Redirect to a desired page after logout
    return redirect('/')  # Replace 'home' with the name of the URL you want to redirect to


def vehicle_index(request):

    data=Vehicle.objects.filter(created_by_id=request.user.id).all()
    compact={'data':data}

    return render(request, 'vehicle/index.html',compact)

def vehicle_create(request):

    if request.method == "POST":
        vehicle_type = request.POST['vehicle_type']
        make = request.POST['make']
        model = request.POST['model']
        year = request.POST['year']
        capacity = request.POST['capacity']


        license_plate = request.POST['license_plate']  # Optional field
        image = request.FILES['image']  # Optional field

        current_date = timezone.now()
        user = request.user

        vehicle = Vehicle.objects.create(
                    vehicle_type=vehicle_type,
                    make=make,
                    model=model,
                    year=year,
                    capacity=capacity,
                    license_plate=license_plate,
                    image=image,
                    created_by=user,
                    updated_by=user
                )

        return redirect('/vehicle_index/')

    return render(request, 'vehicle/create.html')

def vehicle_edit(request,id):
    vehicle = get_object_or_404(Vehicle, id=id)

    current_date = timezone.now()
    user = request.user
    if request.method == 'POST':
        vehicle.vehicle_type = request.POST['vehicle_type']
        vehicle.model = request.POST['model']
        vehicle.license_plate = request.POST['license_plate']
        vehicle.make = request.POST['make']
        vehicle.year = request.POST['year']
        vehicle.capacity = request.POST['capacity']
        vehicle.updated_by=user
        if 'image' in request.FILES:
            vehicle.image = request.FILES['image']
        vehicle.save()
        return redirect('/vehicle_index/')  # Redirect to vehicle list or any other page after saving
    return render(request, 'vehicle/edit.html', {'vehicle': vehicle})


def driver_index(request):

    data=Driver.objects.filter(created_by_id=request.user.id).all()
    compact={'data':data}

    return render(request, 'driver/index.html',compact)


def driver_create(request):

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        license_number = request.POST['license_number']

        current_date = timezone.now()
        user = request.user

        driver = Driver.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    license_number=license_number,
                    created_by=user,
                    updated_by=user
                )

        return redirect('/driver_index/')

    return render(request, 'driver/create.html')


def consignment_index(request):

    data=Consignment.objects.filter(created_by_id=request.user.id).all()
    compact={'data':data}

    return render(request, 'consignment/index.html',compact)


def consignment_create(request):


    current_date = timezone.now()
    user = request.user

    if request.method == "POST":

        sender_name = request.POST['sender_name']
        receiver_name = request.POST['receiver_name']
        weight = request.POST['weight']
        vehicle = request.POST['vehicle']
        dispatch_date = request.POST['dispatch_date']
        status = request.POST['status']
        sender_address = request.POST['sender_address']
        receiver_address = request.POST['receiver_address']
        contents = request.POST['contents']
        driver = request.POST['driver']
        delivery_date = request.POST['delivery_date']

        created_by=user,
        updated_by=user

        vehicle_data = Vehicle.objects.get(id=vehicle)
        driver_data = Driver.objects.get(id=driver)


        consignment = Consignment.objects.create(
                    sender_name=sender_name,
                    receiver_name=receiver_name,
                    weight=weight,
                    vehicle=vehicle_data,
                    dispatch_date=dispatch_date,
                    status=status,
                    sender_address=sender_address,
                    receiver_address=receiver_address,
                    contents=contents,
                    driver=driver_data,
                    delivery_date=delivery_date,
                    created_by=user,
                    updated_by=user
                )

        return redirect('/consignment_index/')

    
    vehicle_data=Vehicle.objects.all()
    driver_data=Driver.objects.all()

    compact={'vehicle_data':vehicle_data, 'driver_data':driver_data}
    return render(request, 'consignment/create.html', compact)

def consignment_edit(request, id):
    consignment = get_object_or_404(Consignment, id=id)
    vehicles = Vehicle.objects.all()
    drivers = Driver.objects.all()

    if request.method == "POST":

        consignment.sender_name = request.POST['sender_name']
        consignment.receiver_name = request.POST['receiver_name']
        consignment.sender_address = request.POST['sender_address']
        consignment.receiver_address = request.POST['receiver_address']
        consignment.weight = request.POST['weight']
        consignment.contents = request.POST['contents']
        consignment.status = request.POST['status']
        consignment.dispatch_date = request.POST['dispatch_date']
        consignment.delivery_date = request.POST['delivery_date']

        vehicle_id = request.POST.get('vehicle')
        consignment.vehicle = Vehicle.objects.get(pk=vehicle_id) if vehicle_id else None

        driver_id = request.POST.get('driver')
        consignment.driver = Driver.objects.get(pk=driver_id) if driver_id else None

        consignment.updated_by = request.user
        consignment.save()

        return redirect('/consignment_index/')  # Replace with the actual dashboard or details view

    context = {
        'consignment': consignment,
        'vehicle_data': vehicles,
        'driver_data': drivers,
    }
    return render(request, 'consignment/edit.html', context)

def consignment_show(request, id):
    consignment = get_object_or_404(Consignment, id=id)
    context = {
        'consignment': consignment,
    }
    return render(request, 'consignment/show.html', context)

def admindashboard(request):
    return render(request,'admin/admindashboard.html')


def all_vehicle(request):

    data=Vehicle.objects.all()
    compact={'data':data}

    return render(request, 'admin/all_vehicle.html',compact)

def all_driver(request):

    data=Driver.objects.all()
    compact={'data':data}

    return render(request, 'admin/all_driver.html',compact)

def all_consignment(request):

    data=Consignment.objects.all()
    compact={'data':data}

    return render(request, 'admin/all_consignment.html',compact)

def report(request):

    current_year = datetime.now().year

    data = Consignment.objects.filter(dispatch_date__year=current_year).values('dispatch_date__month', 'status').annotate(count=Count('id')).order_by('dispatch_date__month')

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    pending_counts = [0] * 12
    approved_counts = [0] * 12
    rejected_counts = [0] * 12
    
    for entry in data:
        month_index = entry['dispatch_date__month'] - 1  
        status = entry['status']
        
        if status == 'Pending':
            pending_counts[month_index] = entry['count']
        elif status == 'Approved':
            approved_counts[month_index] = entry['count']
        elif status == 'Rejected':
            rejected_counts[month_index] = entry['count']
    


    vehicle_type_counts = Vehicle.objects.values('vehicle_type').annotate(count=Count('vehicle_type')).order_by('vehicle_type')
    
    # Prepare data for the chart
    vehicle_types = [item['vehicle_type'] for item in vehicle_type_counts]
    vehicle_counts = [item['count'] for item in vehicle_type_counts]

    context = {
        'months': months,
        'pending_counts': pending_counts,
        'approved_counts': approved_counts,
        'rejected_counts': rejected_counts,
        'vehicle_types': vehicle_types,
        'vehicle_counts': vehicle_counts
    }
    return render(request,'admin/report.html', context)