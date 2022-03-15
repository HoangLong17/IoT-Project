from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
urlpatterns = [
    path('home/', views.home, name='home'),
    path('video_feed/', views.video_feed, name='video-feed'),
    path('capture/',views.capture, name='capture'),
    path('connect/',views.connect, name='connect'),
    path('disconnect/',views.disconnect, name='disconnect'),
    path('',auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/',auth_views.LogoutView.as_view(next_page=''),name="logout"),
    path('Init/', views.Init, name='Init'),
]