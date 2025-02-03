from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="home"),
    path("login/",views.loginview,name="login"),
    path("register/",views.register,name="register"),
    path("resetpassword/",views.reset_password,name="reset_password"),
    path("forgotPassword/",views.forgot_password,name="forgot_password"),
    path("Verifyotp/",views.verify_otp,name="verify_otp"),
    path('logout/', views.logoutview, name='logout'),


    
    
]

