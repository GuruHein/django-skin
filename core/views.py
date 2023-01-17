from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Request, Response
from django_filters import rest_framework as filters
from .filter_backend import CustomFilterBackend

class BaseGenericAPIView(GenericAPIView):
    
    filter_backends = (CustomFilterBackend,)
    prefetch_related_fields = []
    select_related_fields = []
    filterset_fields = "__all__"
    
    def get_queryset(self):
        return self.model.objects.all().prefetch_related(*self.prefetch_related_fields).select_related(*self.select_related_fields)
    
    def order_queryset(self, queryset):
        sorts = self.get_sorts_params()
        return queryset.order_by(*sorts)
    
    def get_sorts_params(self):
        params = self.request.query_params.get('sorts', '')
        if params:
            sorts = params.split(',')
            rmv_sign_sort = [sort.replace("-", "") for sort in sorts]
            # need to validate sorts params
            return sorts
        return []
    
    def send_response(self, success: bool, message=None, results={},  **kwargs):
        success_info = {
            'success': success,
            'message': message,
        }
        response_results = {**success_info, **results}
        return Response(response_results, **kwargs)
        
    
class BaseListGenericAPIView(BaseGenericAPIView):
    name = "Base List View"
    
    def get(self, request: Request):
        queryset = self.order_queryset(self.filter_queryset(self.get_queryset()))
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        if page is not None:
            return self.send_response(
                'True',
                f'List of {self.model.__name__}',
                self.get_paginated_response(data=serializer.data),
                status=status.HTTP_200_OK
            )
            
        return self.send_response(
            True, 
            f'List of {self.model.__name__}',
            serializer.data, 
            status=status.HTTP_200_OK
        )
        
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response(
                            True, 
                            f'{self.model.__name__} is created',
                            serializer.data,  
                            status=status.HTTP_201_CREATED,
                            )
        return self.send_response(
            False,
            f'{self.model.__name__} is not created',
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class BaseDetailsGenericAPIView(BaseGenericAPIView):
    pass