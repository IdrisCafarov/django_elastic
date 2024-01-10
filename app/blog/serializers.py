from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *
import json


class ProfessorDocumentSerializer(DocumentSerializer):
    class Meta(object):
        document = ProfessorDocument
        fields = '__all__'