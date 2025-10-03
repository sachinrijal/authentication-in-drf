from django.urls import path,include
from .views import UserRegistrationView,LoginView,UserprofileView,ChangepasswordView,ResetemailView,UserpasswordresetView


urlpatterns = [
    path('user/register', UserRegistrationView.as_view() ),
    path('user/login', LoginView.as_view() ),
    path('user/profile', UserprofileView.as_view() ),
    path('user/change-password', ChangepasswordView.as_view() ),
    path('user/reset-password', ResetemailView.as_view() ),
    path('user/<uid>/<token>/',UserpasswordresetView.as_view() ),

]