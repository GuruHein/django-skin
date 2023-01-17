from core.serializers import BaseModelSerializer
from .models import Student

class StudentSerializer(BaseModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'