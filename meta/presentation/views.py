from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from meta.application.services import CountryService
from meta.presentation.serializers import CountrySerializer
from drf_spectacular.utils import extend_schema

class CountryListAPIView(GenericAPIView):
    serializer_class = CountrySerializer

    @extend_schema(operation_id="list_countries")
    def get(self, request):
        countries = CountryService().get_all_countries()
        return Response(countries)
    
class CountryDetailAPIView(GenericAPIView):
    serializer_class = CountrySerializer

    @extend_schema(operation_id="retrieve_country")
    def get(self, request, code: str):
        country = CountryService().get_country(code)
        return Response(country)