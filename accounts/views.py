from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from smtplib import SMTPException
from .forms import CustomUserCreationForm
from .verification import send_email_verification, email_verification_token


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            try:
                send_email_verification(request, user)
                messages.add_message(request, messages.SUCCESS,
                                     message="Bienvenue sur Docmachin, un email de confirmation a été envoyé.")
            except SMTPException:
                messages.add_message(request, messages.ERROR, 
                                     message="Oups, l'email n'est pas parti merci de nous contacter à l'adresse")
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "accounts/signup.html", {"form": form})


def activate(request, uidb64, token):
    User = get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    
    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, "Votre compte est activé")
        return redirect("home")
    else:
        messages.add_message(request, messages.ERROR, "Lien plus valide")
        return redirect("home")
    
    
