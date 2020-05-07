from django.urls import path

from . import views

app_name = 'zgg_user'

urlpatterns = [
    path('zgg/user/add', views.user_add, name='add'),
    path('edit/', views.edit_p1, name='edit'),
]