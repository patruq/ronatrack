from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import SurveySerializer
from ..models import Survey

class SurveyViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
    lookup_field = "name"