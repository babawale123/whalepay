from django.urls import path
from note.views import CreateAndGetNote,details

urlpatterns = [
    path('',CreateAndGetNote.as_view()),
    path('details/<int:pk>/',details.as_view()),
]