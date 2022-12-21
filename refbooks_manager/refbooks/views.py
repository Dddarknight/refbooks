import datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from refbooks_manager.refbooks.mixins import LatestVersionMixin
from refbooks_manager.refbooks.models import (
    RefBook, Element
)
from refbooks_manager.refbooks.renderers import AppJSONRenderer
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
    renderer_classes = (AppJSONRenderer, )
    date = openapi.Parameter('date',
                             openapi.IN_QUERY,
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
            return refbooks
        try:
            date = datetime.date.fromisoformat(date_iso)
        except Exception:
            return Response('Date is invalid')
        refbooks = RefBook.objects.filter(
            version__start_date__gte=date).distinct()
        return refbooks


class RefBookElementsView(LatestVersionMixin, ListAPIView):
    """
    Returns a list of elements for a particular RefBook in the latest version.

    If a version parameter is provided, only elements
    of this version of the RefBook will be returned.
    """

    serializer_class = ElementSerializer
    renderer_classes = (AppJSONRenderer, )
    version = openapi.Parameter('version',
                                openapi.IN_QUERY,
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
        version_qp = self.request.query_params.get('version')
        version = version_qp if version_qp else self.get_latest_version(pk)
        elements = elements.filter(version__version=version)
        return elements


class ValidateElementView(LatestVersionMixin, APIView):
    """
    Checks if the element with given parameters exists.

    The code and value parameters are required.
    If a version parameter is absent,
    the element will be checked in the latest version.
    """

    code = openapi.Parameter('code',
                             openapi.IN_QUERY,
                             description="The code of the requested element.",
                             type=openapi.TYPE_STRING,
                             required=True)
    value = openapi.Parameter('value',
                              openapi.IN_QUERY,
                              description="The value of the "
                                          "requested element.",
                              type=openapi.TYPE_STRING,
                              required=True)
    version = openapi.Parameter('version',
                                openapi.IN_QUERY,
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

        elements = Element.objects.filter(
                code=code, value=value, version__refbook__pk=pk
        )
        version_qp = self.request.query_params.get('version')
        version = version_qp if version_qp else self.get_latest_version(pk)
        element = elements.filter(version__version=version)
        return Response(
            f'Element is in RefBook {pk}') if element else Response(
            f'No such Element in RefBook {pk}'
        )
