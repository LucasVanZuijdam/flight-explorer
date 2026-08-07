from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from flights.models import Airport, FlightSearch
from .serializers import AirportSerializer, SearchSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})

@api_view(["GET"])
def airports(request):
    query = request.query_params.get("query", "")

    airport_queryset = Airport.objects.filter(
        Q(city__icontains=query)
    )

    if query:
        airport_queryset = airport_queryset.filter(
            Q(city__icontains=query)
            | Q(name__icontains=query)
            | Q(iata_code__icontains=query)
        )

    serializer = AirportSerializer(
        airport_queryset,
        many=True,
    )

    return Response(serializer.data)

@api_view(["POST"])
def create_search(request):
    serializer = SearchSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            serializer.data,
            status=201,
        )

    return Response(
        serializer.errors,
        status=400,
    )

@api_view(["GET"])
def get_search(request, search_id):
    search = get_object_or_404(
        FlightSearch,
        id=search_id,
    )

    serializer = SearchSerializer(search)

    return Response(serializer.data)

