import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class CommandeFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_creation", lookup_expr='gte')
	end_date = DateFilter(field_name="date_creation", lookup_expr='lte')
	note = CharFilter(field_name='note', lookup_expr='icontains')


	class Meta:
		model = Commande
		fields = '__all__'
		exclude = ['client', 'date_creation']