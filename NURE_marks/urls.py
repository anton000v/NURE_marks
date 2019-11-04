from django.urls import path, include
from . import views
from django.views.static import serve
from NURE_marks_engine import settings

urlpatterns = [
    path('', views.main_screen),
    path('accounts/', include('allauth.urls')),
    path('login/', views.user_login, name='user_login'),
    # url(r'^flexselect/', include('flexselect.urls')),
    # path('flexselect/', include('flexselect.urls')),
    # url(r'^chaining/', include('smart_selects.urls')),
    path('chaining/', include('smart_selects.urls')),
    path('group/<int:group_pk>-<int:subject_pk>', views.group_detail, name='group_detail'),
    path('group/<int:group_pk>-<int:subject_pk>/group_marks_edit', views.group_marks_edit, name='group_marks_edit')
    # path('media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),
    # path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}),
]
