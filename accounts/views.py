from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration completed successfully.")
            return redirect("home")

    else:
        form = UserRegistrationForm()

    context = {
        "form": form,
    }

    return render(request, "accounts/register.html", context)


@login_required
def profile(request):
    return render(request, "accounts/profile.html")