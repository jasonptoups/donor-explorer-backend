from django.urls import path
from . import views

urlpatterns = [
    path('saved-donors',
         views.SavedDonorList.as_view(),
         name='saved-donor-list'),

    path('saved-donors/<int:pk>',
         views.SavedDonorDetail.as_view(),
         name='saved-donor-detail'),

    path('users',
         views.UserList.as_view(),
         name='users-list'),

    path('users/register',
         views.CreateAuth.as_view(),
         name='users-register'),

    path('users/<int:pk>',
         views.UserDetail.as_view(),
         name='user-detail')
]
