import django_filters
from django_filters import CharFilter
from .models import *


class AssetFilter(django_filters.FilterSet):
    asset_serial = CharFilter(label='Serial No.',
                              field_name="asset_serial", lookup_expr="icontains")
    assettype__name = CharFilter(label='Asset Type',
                                 field_name="assettype__name", lookup_expr="icontains")
    region__name = CharFilter(label='Region',
                              field_name="region__name", lookup_expr="icontains")
    station__name = CharFilter(label='Station',
                               field_name="station__name", lookup_expr="icontains")

    class Meta:
        model = Comp
        fields = ['asset_serial', 'assettype__name',
                  'region__name', 'station__name']
