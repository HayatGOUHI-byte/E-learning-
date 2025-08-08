from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from blog.models import Instructor
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, InstructorRegisterForm, StudentRegisterForm, \
    ContactForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profileupdate(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile-page')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile_update.html', context)


def beinstructor(request):
    if request.method == 'POST':
        form = InstructorRegisterForm(request.POST,
                                      request.FILES)
        form.fields["user"].initial = request.user
        form.fields["user"].disabled = True
        if form.is_valid():

            form.save()
            messages.success(request, f'Well received. Check your Email for more informations. ')
            return redirect('landing-page')
    else:
        form = InstructorRegisterForm(instance=request.user)
        form.fields["user"].initial = request.user
        form.fields["user"].disabled = True
    return render(request, 'users/be_instructor.html', {'form': form})


def bestudent(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST,
                                   request.FILES)
        form.fields["user"].initial = request.user
        form.fields["user"].disabled = True
        if form.is_valid():
            form.save()
            messages.success(request, f'Well received. Check your Email for more informations. ')
            return redirect('landing-page')
    else:
        form = StudentRegisterForm()
        form.fields["user"].initial = request.user
        form.fields["user"].disabled = True
    return render(request, 'users/be_student.html', {'form': form})


def team(request):
    return render(request, 'users/team.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email_address']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            admin = settings.EMAIL_HOST_USER
            message = 'name : ' + name + '\nfrom: ' + email + '\nmessage\n' + message
            try:
                send_mail(subject, message, email, [admin], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("/contact/")

    form = ContactForm()
    return render(request, "users/contact.html", {'form': form})
