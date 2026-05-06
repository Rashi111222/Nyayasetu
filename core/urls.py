from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_judgment, name='upload'),
    path('review/<int:pk>/', views.review_plan, name='review_plan'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
] 
