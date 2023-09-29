from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Utube'),
    path('log', views.login_page, name='login'),
    path('reg', views.reg, name='Register'),
    path('upload', views.uploads, name='upload'),
    path('user_home', views.login_home, name='user_home'),
    path('video-play', views.video_play, name='video-play'),
    path('your_vid', views.user_video, name='your_vid' ),
    path('profile', views.profile, name='profile'),
    path('video_edit', views.v_e, name='video_edit'),
    path('video_delete', views.delete, name='video_delete'),
    path('log-out', views.out, name='log-out'),
    path('category', views.category, name='category'),
    path('search', views.search, name='search'),
]

