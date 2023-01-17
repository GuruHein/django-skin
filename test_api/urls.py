from django.urls import path
from .views import StudentListGenericAPIView

urlpatterns = [
    path('students/', StudentListGenericAPIView.as_view(), name='student-list'),
]