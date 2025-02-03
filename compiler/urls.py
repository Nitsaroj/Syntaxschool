from django.urls import path
from .views import *

urlpatterns=[
    path('compiler/',compiler,name='compiler')    
]