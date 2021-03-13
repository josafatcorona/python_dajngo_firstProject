from django.urls import path, include, re_path
from blog import views


app_name = "blog"

urlpatterns = [
    re_path(r'^login/$',views.user_login, name='user_login'),
    re_path(r'^register/$',views.register, name='register'),
]
