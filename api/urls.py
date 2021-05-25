from django.contrib import admin
from django.urls import path
from api import views

urlpatterns=[

    #项目部分api

    # path('index/', views.run_case_demo),

    path('project/', views.project),
    path('project_update/', views.project_update),
    path('project_delete/', views.project_delete),
    path('project_add/', views.project_add),
]