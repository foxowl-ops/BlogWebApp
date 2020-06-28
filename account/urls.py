from django.urls import path,include
from account.views import SignUpView,UserDetailsView , UserUpdateView, UserDeleteView
urlpatterns = [
    path("", include('django.contrib.auth.urls')),
    path("signup", SignUpView.as_view(), name='signup'),
    path('user_view/<int:id>', UserDetailsView.as_view(), name='detailuser'),
    path("user_update/<int:id>", UserUpdateView.as_view(), name='updateuser'),
    path("user_delete/<int:id>", UserDeleteView.as_view(), name='deleteuser'),
    ]