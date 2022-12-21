import datetime
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.db.models import Subquery
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from refbooks_manager.refbooks.models import (
    RefBook, Version, Element
)
from refbooks_manager.refbooks.serializers import (
    RefBookSerializer, ElementSerializer
)


class RefBooksView(ListAPIView):
    """
    Returns a list of all refbooks.

    If a date parameter is provided, the refbooks which have versions
    with started date after the requested date will be returned.
    """

    serializer_class = RefBookSerializer
    date = openapi.Parameter('date', openapi.IN_QUERY,
                             description="The refbooks which have versions "
                                         "with started date after the "
                                         "requested date will be returned.",
                             type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[date])
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        date_iso = self.request.query_params.get('date')
        if not date_iso:
            refbooks = RefBook.objects.all()
        else:
            try:
                date = datetime.date.fromisoformat(date_iso)
            except Exception:
                return Response('Date is invalid')
            refbooks = RefBook.objects.filter(
                version__start_date__gte=date).distinct()
        return refbooks


class RefBookElementsView(ListAPIView):
    """
    Returns a list of elements for a particular RefBook in the latest version.

    If a version parameter is provided, only elements
    of this version of the RefBook will be returned.
    """

    serializer_class = ElementSerializer
    version = openapi.Parameter('version', openapi.IN_QUERY,
                                description="The value of the RefBook version."
                                            "Only elements of this version"
                                            " of the RefBook are returned",
                                type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[version])
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        elements = Element.objects.filter(version__refbook__pk=pk)
        version = self.request.query_params.get('version')
        if version:
            elements = elements.filter(version__version=version)
        else:
            ordered_versions = Version.objects.filter(
                refbook__pk=pk,
                start_date__lte=datetime.date.today()
            ).order_by("-start_date")
            elements = elements.filter(
                version__version=Subquery(
                    ordered_versions.values('version')[:1]))
        return elements


class ValidateElementView(APIView):
    """
    Checks if the element with given parameters exists.

    The code and value parameters are required.
    If a version parameter is absent,
    the element will be checked in the latest version.
    """

    code = openapi.Parameter('code', openapi.IN_QUERY,
                             description="The code of the requested element.",
                             type=openapi.TYPE_STRING,
                             required=True)
    value = openapi.Parameter('value', openapi.IN_QUERY,
                              description="The value of the "
                                          "requested element.",
                              type=openapi.TYPE_STRING,
                              required=True)
    version = openapi.Parameter('version', openapi.IN_QUERY,
                                description="The value of the RefBook version."
                                            "Only elements of this version"
                                            " of the RefBook are returned",
                                type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[code, value, version])
    def get(self, request, pk):
        code = self.request.query_params.get('code')
        value = self.request.query_params.get('value')
        if not code or not value:
            return Response('Request data is invalid')
        version = self.request.query_params.get('version')
        elements = Element.objects.filter(
                code=code, value=value, version__refbook__pk=pk
        )
        if version:
            element = elements.filter(version__version=version)
        else:
            ordered_versions = Version.objects.filter(
                refbook__pk=pk,
                start_date__lte=datetime.date.today()
            ).order_by("-start_date")
            element = elements.filter(
                version__version=Subquery(
                    ordered_versions.values('version')[:1])
            )
        return Response(
            f'Element is in RefBook {pk}') if element else Response(
            f'No such Element in RefBook {pk}'
        )
