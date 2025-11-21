import django_filters

from .models import Ad


class AdFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    price = django_filters.CharFilter(field_name="price", lookup_expr="icontains")
    description = django_filters.CharFilter(
        field_name="description", lookup_expr="icontains"
    )

    class Meta:
        model = Ad
        fields = ["title", "price", "description"]
