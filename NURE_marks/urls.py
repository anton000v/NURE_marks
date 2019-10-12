from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_screen),
    path('accounts/', include('allauth.urls')),
    path('login/', views.user_login, name='user_login'),
    # url(r'^flexselect/', include('flexselect.urls')),
    # path('flexselect/', include('flexselect.urls')),
# url(r'^chaining/', include('smart_selects.urls')),
    path('chaining/',include('smart_selects.urls')),
]
