#==>Library Import
from django.urls import path
#==>Local Import
from . import views


app_name='account'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-phone/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('address/', views.AddressView.as_view(), name='profile_address'),
    path('update-phone/', views.UpdatePhoneNumberView.as_view(), name='update_phone'),
    path('change-username/', views.ChangeUsernameView.as_view(), name='change_username'),
    path('activate-email/', views.SendActivateEmailView.as_view(), name='email-activate'),
    path('activate/<uidb64>/<token>/<email>/', views.ActivateEmailView.as_view(), name='activate'),
    path('reset-password/', views.UserPasswordResetView.as_view(), name='reset_password'),
	path('reset-password/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
	path('confirm-password/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('confirm-password/complete', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

