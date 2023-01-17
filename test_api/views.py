from django_filters import rest_framework as filters
from core.views import BaseListGenericAPIView
from .models import Student
from .serializers import StudentSerializer

# class StudentFilter(filters.FilterSet):
#     min_age = filters.NumberFilter(field_name="age", lookup_expr='gte')
#     max_age = filters.NumberFilter(field_name="age", lookup_expr='lte')

#     class Meta:
#         model = Student
#         fields = ['name']

# Create your views here.
class StudentListGenericAPIView(BaseListGenericAPIView):
    model = Student
    serializer_class = StudentSerializer
    # filterset_fields = ("name", "age")
    # filterset_class = StudentFilter