from .views import *
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('alterpost/<int:pk>/', FetchUpdateDeleteView.as_view(),name="alter_post"),
    path("post/", CreatePostAPIView.as_view(), name="create_and_view_posts"), 
    path("searchposts/", SearchFilterAPIView.as_view(), name="search_post"),
]

