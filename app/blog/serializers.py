from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from blog.documents.professor_index import *
import json


class ProfessorDocumentSerializer(DocumentSerializer):


    highlight = serializers.SerializerMethodField()


    class Meta(object):
        document = ProfessorDocument
        fields = '__all__'

    def get_highlight(self, obj):
        # This method retrieves the highlight field from the Elasticsearch response
        return obj.meta.highlight.to_dict() if hasattr(obj.meta, 'highlight') else {}

