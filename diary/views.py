from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from diary.forms import SignUpForm, DiaryForm, UserLoginForm, UpdateProfile, ContactForm
from diary.models import Registration, Diary


def home(request):
    return render(request, 'home.html')


def test(request):
    return render(request, 'index.html')


def public(request):
    today = timezone.now().date()
    queryset_list = Diary.objects.public()

    context = {
        "object_list": queryset_list,
        "title": "List",
        "today": today,
    }
    return render(request, "diary_list.html", context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST, request.FILES)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse("Your account was inactive.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username, password))
                return HttpResponse("Invalid login details given")
        else:
            return HttpResponse("Correct Your forms")

    else:
        form = UserLoginForm()

        return render(request, 'register.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            print(email)
            if not Registration.objects.filter(username=username).exists():
                Registration.objects.create_user(username, email, raw_password)

                pw = form.cleaned_data.get
                name = pw('name')
                gender = pw('gender')
                dob = pw('dob')
                mobile_num = pw('mobile_num')
                telephone = pw('telephone')
                photo = pw('photo')

                obj = Registration.objects.get(username=username)
                obj.gender = gender
                obj.dob = dob
                obj.name = name
                obj.mobile_num = mobile_num
                obj.telephone = telephone
                obj.photo = photo
                obj.save()

                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
        else:
            return HttpResponse("Correct Your forms")
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = UpdateProfile()

    return render(request, 'register.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


def diary_create(request):
    form = DiaryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        if request.user.is_superuser:
            instance.is_public = True
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect('/')
    context = {
        "form": form,
    }
    return render(request, "diary_form.html", context)


def contact(request):
    title = "CONTACT ME"
    if request.method == "POST":
        print(request.POST)
    form = ContactForm(request.POST or None)
    context = {
        "form": form,
        "title": title,
    }
    if form.is_valid():
        instance = form.save()
        print(instance)
        instance.save()
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')
        full_name = form.cleaned_data.get('full_name')
        messages.success(request, "Successfully Sent. Thanking You for Contacting Me")
        print(email, message, full_name)
        return HttpResponseRedirect('/')

        # send_mail(
        #     subject="Contact",
        #     message=message,
        #     from_email=email,
        #     recipient_list=['aswin@xeoscript.com']
        # )

    return render(request, "forms.html", context)


def diary_list(request):
    today = timezone.now().date()
    queryset_list = Diary.objects.filter(user=request.user)  # .order_by("-timestamp")
    context = {
        "object_list": queryset_list,
        "title": "List",
        "today": today,
    }
    return render(request, "diary_list.html", context)


def diary_detail(request, id=None):
    instance = get_object_or_404(Diary, id=id)

    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "diary_detail.html", context)


def diary_update(request, id=None):
    instance = get_object_or_404(Diary, id=id)
    if instance.user == request.user:
        form = DiaryForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Item Saved", extra_tags='html_safe')
            return HttpResponseRedirect('/')

        context = {
            "title": instance.title,
            "instance": instance,
            "form": form,
        }
        return render(request, "diary_form.html", context)

    else:
        messages.error(request, "You Dont have permission to edit")
        return HttpResponseRedirect('/')


def diary_delete(request, id=None):
    instance = get_object_or_404(Diary, id=id)
    if instance.user == request.user:
        instance.delete()
        messages.success(request, "Successfully deleted")
    else:
        messages.error(request, "You Dont have permission to delete")

    return HttpResponseRedirect('/')
