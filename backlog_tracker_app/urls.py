from django.urls import path
from backlog_tracker_app import views
from django.conf.urls import include

app_name = 'backlog_tracker_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('user_login/', views.user_login, name='user_login'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('show/<int:show_id>/', views.show, name='show'), 
    path('update_account/', views.update_account, name='update_account'), 
    path('backlog/', views.backlog, name='backlog'), 
    path('add_backlog/<int:show_id>/', views.add_backlog, name='add_backlog')
]
