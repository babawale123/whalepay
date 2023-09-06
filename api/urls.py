from django.urls import path
from api.views import SignUp,Login

urlpatterns = [
    path('',SignUp),
    path('login/',Login)
]