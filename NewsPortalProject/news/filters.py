from django.forms import DateInput
from django_filters import FilterSet, CharFilter, DateFilter, ModelMultipleChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):
    heading = CharFilter(
        lookup_expr='contains',
        label='Name',
    )
    date = DateFilter(
        lookup_expr='gt',
        widget=DateInput(
            attrs={'type': 'date'}
                         ),
        label='Date',
    )
    categories = ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),

    )
    class Model:
        model = Post
        fields = [
            'categories',
        ]

