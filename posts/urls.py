from django.urls import path
from .import views
from posts.views import UserFormView



urlpatterns = [
    path('create/', views.post_create, name = 'post_create'),
    path('detail/<int:id>/', views.post_detail, name='post_detail'),
    path('list/', views.post_list, name = 'post_list'),
    path('<int:id>/edit/', views.post_update, name='post_update'),
    path('<int:id>/delete/', views.post_delete, name = 'post_delete'),
    path('register/',UserFormView.as_view(), name = 'register'),

]
