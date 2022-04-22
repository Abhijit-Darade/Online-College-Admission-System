from email import message
import email
from operator import index
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import ApplicationForm
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from .models import Application, Notice, Detail
from django.views.generic import UpdateView

#email
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from home.forms import CreateUserForm
# from django.contrib.auth.forms import CreateUserForm
# from django.contrib.auth.decorators import login_required
# from .models import Destination

def index(request):
   if request.user.is_anonymous:
      return redirect("/login")
   return render(request, 'index.html')


def loginUser(request):
   if request.user.is_authenticated:
      return redirect('home')
   else:
      if request.method == "POST":
         username = request.POST.get('username')
         password = request.POST.get('password')
         print(username, password)
      # check if user has entered correct credentials
         user = authenticate(username=username, password=password)
         if username=="Admin" and password=="Admin":
            login(request,user)
            return redirect("/handle_admin")
         elif user is not None:
            #A backend authenticated the credentials
            login(request, user)
            return redirect("/")
         else:
            #No backend authenticated the credentials
            messages.info(request, 'Username OR password is incorrect')
            return render(request, 'login.html')
      return render(request, 'login.html')


def logoutuser(request):
   logout(request)
   return redirect('/login')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


def application_form(request):

   if not request.user.is_authenticated:
        return redirect("/login")
   hide = Application.objects.filter(user=request.user)
   if request.method == "POST":
      form = ApplicationForm(request.POST, request.FILES)
      if form.is_valid():
         application = form.save()
         application.user = request.user
         application.save()
         return render(request, "application_form.html")
   else:
      form = ApplicationForm()
   return render(request, "application_form.html", {'form': form, 'hide': hide})


class UpdatePostView(UpdateView):
    model = Application
    template_name = 'application_status.html'
    fields = ('Application_Status', 'message',)


def approved_applications(request):
    if not request.user.is_superuser:
        return redirect("/login")
    approved = Application.objects.filter(Application_Status="Approved")
    return render(request, "approved_applications.html", {'approved': approved})


def edit_application(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    try:
        application = request.user.application
    except Application.DoesNotExist:
        application = Application(user=request.user)
    if request.method == "POST":
        form = ApplicationForm(
            data=request.POST, files=request.FILES, instance=application)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "edit_application.html/", {'alert': alert})
    else:
        form = ApplicationForm(instance=application)
    return render(request, "edit_application.html/", {'form': form})


def status(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    application = Application.objects.get(user=request.user)
    return render(request, "status.html", {'application': application})


def pending_applications(request):
    if not request.user.is_superuser:
        return redirect("/login")
    pending = Application.objects.filter(Application_Status="Pending")
    return render(request, "pending_applications.html", {'pending': pending})


def rejected_applications(request):
    if not request.user.is_superuser:
        return redirect("/login")
    rejected = Application.objects.filter(Application_Status="Rejected")
    return render(request, "rejected_applications.html", {'rejected': rejected})


def handle_admin(request):
    if not request.user.is_superuser:
        return redirect("/login")
    users = User.objects.all().count
    approve = Application.objects.filter(Application_Status='Approved').count
    reject = Application.objects.filter(Application_Status='Rejected').count
    pending = Application.objects.filter(Application_Status='Pending').count
    return render(request, "handle_admin.html", {'approve': approve, 'reject': reject, 'pending': pending, 'users': users})

    if Application == 'approve':
        subject = 'Welcome to VIT'
        message = f'Hi {user.username}, Your Application Is Approved. You can come to college after 3 days with your original documents to verify at college. Thank You '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list)


def users(request):
    if not request.user.is_superuser:
        return redirect("/login")
    allUsers = Application.objects.all()
    return render(request, "users.html", {'allUsers': allUsers})


def student_application(request, myid):
    if not request.user.is_superuser:
        return redirect("/login")
    application = Application.objects.filter(id=myid)
    return render(request, "student_application.html", {'application': application[0]})


