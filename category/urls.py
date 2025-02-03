from django.urls import path
from .views import *

urlpatterns=[
     path('category/',category_view, name='category'),
    path('category/<str:category_name>/',topic_view, name='topic'),
    path('category/<str:category_name>/<str:topic_name>/', lesson_view, name='lesson'),
    path('category/<str:category_name>/<str:topic_name>/<str:lesson_name>/',lesson_detail,name='lesson_detail'),    
    path('category/<str:category_name>/<str:topic_name>/<str:lesson_name>/<str:view_type>/',lesson_detail,name='lesson_detail')    
]