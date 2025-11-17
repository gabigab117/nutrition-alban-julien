from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import signup_view, activate, profile_view


app_name = "accounts"
urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("profile/", profile_view, name="profile"),
    path("login/", auth_views.LoginView.as_view(
        template_name="accounts/login.html",
        next_page=reverse_lazy("accounts:profile")
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(
        next_page=reverse_lazy("home")
    ), name="logout"),
    path("password_change", auth_views.PasswordChangeView.as_view(
        template_name="password/password_change.html",
        success_url=reverse_lazy("accounts:password_change_done")), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="password/password_change_done.html"), name="password_change_done")
]
