from django.shortcuts import render, HttpResponse, redirect,Http404,get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Contact,Single,TeamCook,Booking, Payment
from .forms import BookingForm, ContactForm,SingleRegistrationForm, TeamCookRegistrationForm
import logging
from math import ceil
from django.urls import reverse
import stripe
from reportlab.pdfgen import canvas
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.contrib.auth.hashers import check_password
# from .backends import CookTypeBackend

logger = logging.getLogger(__name__)
# user_type_backend = CookTypeBackend()

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def menu(request):
    return render(request, 'menu.html')

def booking(request):
    return render(request, 'booking.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def details(request):
    return render(request, 'details.html')

def bookView(request):
    return render(request, 'bookView.html')

def checkout(request):
    cook = None
    is_single = False
    cook_id = request.GET.get('cook_id')
    if cook_id:
        try:
            cook = Single.objects.get(id=cook_id)
            is_single = True
        except Single.DoesNotExist:
            try:
                cook = TeamCook.objects.get(id=cook_id)
                is_single = False
            except TeamCook.DoesNotExist:
                messages.error(request, "Cook not found.")
                return redirect('checkout')  

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment')
        else:
            print(form.errors)
            return render(request, 'checkout.html', {'form': form})
    else:
        form = BookingForm()

    return render(request, 'checkout.html', {'form': form, 'cook': cook, 'is_single': is_single})

def payment(request):
    return render(request,'payment.html')

def generate_invoice(request, booking_id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{booking_id}.pdf"'

    p = canvas.Canvas(response)
    # Add your invoice details here
    p.drawString(100, 800, "Invoice")
    p.drawString(100, 780, f"Booking ID: {booking_id}")
    # Add more details as needed
    p.showPage()
    p.save()
    return response
    

@login_required
def success(request):
    return render(request, 'success.html')

@login_required
def download_file(request):
    try:
        payment = Payment.objects.get(user=request.user, status='Completed')
        file_path = 'media/cook/images'
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/force-download")
            response['Content-Disposition'] = f'attachment; filename={file_path.split("/")[-1]}'
            return response
    except Payment.DoesNotExist:
        raise Http404("No completed payment found for this user.")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = Contact.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )
            # Save the contact instance (not needed since create() already saves it)
            # contact.save()
            
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # Redirect back to the contact page after successful submission
    else:
        form = ContactForm()  # Instantiate a blank form for GET requests
    
    return render(request, 'contact.html', {'form': form}) 

def team(request):
    return render(request, 'team.html')

@login_required
def updatesingle(request):
    cook_id = request.GET.get('cook_id')
    if cook_id:
        single = get_object_or_404(Single, id=cook_id)
    else:
        single = get_object_or_404(Single, username=request.user.username)
    
    if request.method == 'POST':
        form = SingleRegistrationForm(request.POST, request.FILES, instance=single)
        if form.is_valid():
            form.save()
            return redirect('viewProfile', id=single.id)  # Redirect to profile page or any other page
    else:
        form = SingleRegistrationForm(instance=single)
    
    return render(request, 'updatesingle.html', {'form': form})


@login_required
def updateteam(request):
    cook_id = request.GET.get('cook_id')
    if cook_id:
        team = get_object_or_404(TeamCook, id=cook_id)
    else:
        team = get_object_or_404(TeamCook, username=request.user.username)
    
    if request.method == 'POST':
        form = TeamCookRegistrationForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect('viewProfile', id=team.id)  # Redirect to profile page or any other page
    else:
        form = TeamCookRegistrationForm(instance=team)
    
    return render(request, 'updateteam.html', {'form': form})


def viewProfile(request, id):
    try:
        # Try to get a Single cook with the given id
        cook = Single.objects.get(id=id)
        is_single = True
    except Single.DoesNotExist:
        try:
            # If Single cook not found, try to get a TeamCook with the given id
            cook = TeamCook.objects.get(id=id)
            is_single = False
        except TeamCook.DoesNotExist:
            # If neither Single nor TeamCook found, raise a 404 error
            raise Http404("Cook does not exist")

    context = {
        'cook': cook,
        'is_single': is_single,
    }
    return render(request, 'viewProfile.html',context)

def cook(request):
    if request.method == 'POST':
        form = SingleRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['name'],
                password=form.cleaned_data['password']
            )
            user.save()
            single_cook = Single.objects.create(
                username=user,
                email=form.cleaned_data['email'],
                experience=form.cleaned_data['experience'],
                speciality=form.cleaned_data['speciality'],
                dish=form.cleaned_data['dish'],
                gender=form.cleaned_data['gender'],
                desc=form.cleaned_data['desc'],
                photo=form.cleaned_data['photo']
            )
            single_cook.save()
            return redirect('singlecookdetails', singlecook_id=single_cook.id)
    else:
        form = SingleRegistrationForm()
    return render(request, 'cook.html', {'form': form})

def teamreg(request):
    if request.method == 'POST':
        form = TeamCookRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['name'],
                password=form.cleaned_data['password']
            )
            user.save()
            team_cook = TeamCook.objects.create(
                username=user,
                email=form.cleaned_data['email'],
                experience=form.cleaned_data['experience'],
                teamName=form.cleaned_data['teamName'],
                dish=form.cleaned_data['dish'],
                people=form.cleaned_data['people'],
                desc=form.cleaned_data['desc'],
                photo=form.cleaned_data['photo']
            )
            team_cook.save()
            return redirect('teamdetails', teamcook_id=team_cook.id)
    else:
        form = TeamCookRegistrationForm()
    return render(request, 'teamreg.html', {'form': form})

def cookalready(request):
    return render(request, 'cookalready.html')

def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for erroneous input
        if len(username) < 3:
            messages.error(request, "Your username must be at least 3 characters long")
            return redirect('/')

        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('/')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('/')

        try:
            # Create the user
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "Your account has been successfully created")
            return redirect('handleLogin')
        except IntegrityError:
            messages.error(request, "Username already exists")
            return redirect('/')

    else:
        return HttpResponse("404 - Not found")

def handleLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('booking')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect('/login/')
    else:
        return render(request, 'login.html') 

    

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

def handleReg(request):
    if request.method == 'POST':
        userType = request.POST.get('userType')
        logger.debug(f"User Type: {userType}")  # Debug statement to log userType
        
        if userType == 'Single':
            return redirect('cook')  # Use named URL
        elif userType == 'Team':
            return redirect('teamreg')  # Use named URL
        else:
            logger.debug("Invalid user type")
            return redirect('handleReg')
    
    return redirect('/')


def handleCook(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")

            # Get the SingleCook instance related to this user
            try:
                single_cook = Single.objects.get(username=user)
                singlecook_id = single_cook.id
                return redirect(reverse('singlecookdetails', args=[singlecook_id]))
            except Single.DoesNotExist:
                messages.error(request, "No Single Cook profile found for this user.")
                return redirect('cookalready')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect('cookalready')
    else:
        return render(request, 'cookalready.html')


def handleTeam(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")

            # Get the SingleCook instance related to this user
            try:
                team_cook = TeamCook.objects.get(username=user)
                teamcook_id = team_cook.id
                return redirect(reverse('teamdetails', args=[teamcook_id]))
            except TeamCook.DoesNotExist:
                messages.error(request, "No Single Cook profile found for this user.")
                return redirect('cookalready')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect('cookalready')
    else:
        return render(request, 'cookalready.html')

    
def singlecookdetails(request, singlecook_id):
    try:
        # Fetch the Single instance using the provided ID
        single_cook = get_object_or_404(Single, id=singlecook_id)
        print(f"Fetching details for user: {single_cook.username}")

        # Log all Single usernames for debugging
        single_usernames = Single.objects.values_list('username', flat=True)
        print(f"All Single usernames in the database: {list(single_usernames)}")

        bookings = Booking.objects.filter(name=single_cook)
        return render(request, 'singlecookdetails.html', {'bookings': bookings, 'single_cook': single_cook})
    except Single.DoesNotExist:
        print(f"Single cook does not exist for ID: {singlecook_id}")
        raise Http404("Single cook does not exist for this ID")


def teamdetails(request, teamcook_id):
    # Assuming there is a relationship between user and team
    try:
        # Fetch the Single instance using the provided ID
        team_cook = get_object_or_404(TeamCook, id=teamcook_id)
        print(f"Fetching details for user: {team_cook.username}")

        # Log all Single usernames for debugging
        team_usernames = TeamCook.objects.values_list('username', flat=True)
        print(f"All Team usernames in the database: {list(team_usernames)}")

        bookings = Booking.objects.filter(name=team_cook)
        return render(request, 'teamdetails.html', {'bookings': bookings, 'team_cook': team_cook})
    except TeamCook.DoesNotExist:
        print(f"Team cook does not exist for ID: {teamcook_id}")
        raise Http404("Team cook does not exist for this ID")

def cookView(request, id):
    try:
        # Try to get a Single cook with the given id
        cook = Single.objects.get(id=id)
        is_single = True
    except Single.DoesNotExist:
        try:
            # If Single cook not found, try to get a TeamCook with the given id
            cook = TeamCook.objects.get(id=id)
            is_single = False
        except TeamCook.DoesNotExist:
            # If neither Single nor TeamCook found, raise a 404 error
            raise Http404("Cook does not exist")

    context = {
        'cook': cook,
        'is_single': is_single,
    }
    return render(request, 'cookView.html', context)

def searchMatch(query, item):
    if query.lower() in item.speciality.lower() or query.lower() in item.dish.lower() or query.lower() in item.desc.lower():
        return True
    return False

def search(request):
    query = request.GET.get('search')
    allCook = []

    # Search in Single model
    single_cooks = Single.objects.all()
    filtered_single_cooks = [item for item in single_cooks if searchMatch(query, item)]
    if filtered_single_cooks:
        n = len(filtered_single_cooks)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allCook.append(['Single', filtered_single_cooks, range(1, nSlides), nSlides])

    # Search in TeamCook model
    team_cooks = TeamCook.objects.all()
    filtered_team_cooks = [item for item in team_cooks if searchMatch(query, item)]
    if filtered_team_cooks:
        n = len(filtered_team_cooks)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allCook.append(['Team', filtered_team_cooks, range(1, nSlides), nSlides])

    params = {'allCook': allCook}
    if len(allCook)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'search.html', params)