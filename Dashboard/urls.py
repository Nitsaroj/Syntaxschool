from django.urls import path
from . import views

urlpatterns=[
    path('profile/', views.profile, name='profile'),
    path('update/', views.update_profile, name='update_profile'),
    path('profile_redirect_view/', views.profile_redirect_view, name='profile_redirect'), 
    path('coin-history/', views.coin_history, name='coin_history'),
]
