from django.contrib import messages
from django.contrib.auth.models import User
import re
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from .models import Customer1

def register(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        contact_number = request.POST.get("contact_number")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not re.fullmatch(r"^\d{10}$", contact_number):
            messages.error(request, "Contact number must be exactly 10 digits.")
            return redirect("userapp:register")

        if not re.fullmatch(r"^(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
            messages.error(request, "Password must be at least 8 characters long, include 1 uppercase letter, and 1 special character.")
            return redirect("userapp:register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("userapp:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect("userapp:register")

        # Create a new user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password  # Django automatically hashes it
        )

        # Create the associated Customer1 instance
        Customer1.objects.create(
            user=user,
            customer_name=customer_name,
            contact_number=contact_number,
            email=email,
            password=make_password(password)  # Optional; you can skip this if using only `User`
        )

        messages.success(request, "Registration successful! You can now log in.")
        return redirect("userapp:login")

    return render(request, "register.html")




from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        

        # Use Django's authenticate function
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log the user in
            auth_login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("movieapp:home")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("userapp:login")

    return render(request, "login.html")


# Logout View
def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("movieapp:home")





# Create your views here.
