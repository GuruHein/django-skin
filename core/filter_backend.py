from django_filters import rest_framework as filters

class CustomFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # merge filterset kwargs provided by view class
        if hasattr(view, 'get_filterset_kwargs'):
            kwargs.update(view.get_filterset_kwargs())
        
        return kwargs