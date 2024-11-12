from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # main app urls
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout
    path('main/', include('main.urls')),  # Include main app URLs
    path('accounts/', include('allauth.urls')), 
     
]

