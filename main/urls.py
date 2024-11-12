from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('courses/', views.courses, name='courses'),
    path('payment/<int:course_id>/', views.payment, name='payment'),
    path('logout/', views.logout_view, name='logout'), 
    path('payment/success/', views.payment_success, name='payment_success'),
]
