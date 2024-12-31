from django.contrib import admin
from django.urls import path
from . import views

app_name = 'movieapp'

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('movie/<int:movie_id>/submit_review/', views.submit_review, name='submit_review'),
]