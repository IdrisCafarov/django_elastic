# search_indexes.py
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
# from .models import Professor
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import FunctionScore, ScriptScore

import ast

# from django_elasticsearch_dsl.fields import ObjectField, URLField

from django.conf import settings

from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion
from django_elasticsearch_dsl_drf.versions import ELASTICSEARCH_GTE_5_0

from blog.models import Professor
from .analyzers import html_strip

__all__ = ('ProfessorDocument',)
# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)




@INDEX.doc_type
class ProfessorDocument(Document):
    """Book Elasticsearch document."""


    

    id = fields.IntegerField(attr='id')

    name = StringField(
        analyzer=html_strip,
        fields={
            'raw': StringField(analyzer='keyword'),
        }
    )

    title = KeywordField()

    

    introduction = StringField(
        analyzer=html_strip,
        fields={
            'raw': StringField(analyzer='keyword'),
        }
    )

    achievements = StringField(
        analyzer=html_strip,
        fields={
            'raw': StringField(analyzer='keyword'),
        }
    )

    city = KeywordField()

    province = StringField(
        analyzer=html_strip,
        fields={
            'raw': StringField(analyzer='keyword'),
        }
    )

    country = StringField(
        analyzer=html_strip,
        fields={
            'raw': StringField(analyzer='keyword'),
        }
    )

    
    research_areas = StringField(
        analyzer=html_strip,
        fields={
            'raw': StringField(analyzer='keyword'),
        }
    )


    university = KeywordField()

    department = StringField(
        analyzer=html_strip,
        fields={
            'raw': StringField(analyzer='keyword'),
        }
    )

    image_url = StringField()
    public = fields.BooleanField()
    email = StringField()
    phone = StringField()
    address = StringField()
    slug = KeywordField(index=False, store=True)
    suggest = fields.CompletionField()
    non_empty_field_count = fields.IntegerField(attr="get_non_empty_field_count")
    rating = fields.FloatField()

    

    class Django(object):
        model = Professor  # The model associate with this Document


    class Meta:
        parallel_indexing = True
        # queryset_pagination = 50  # This will split the queryset
        #                           # into parts while indexing

    def prepare_suggest(self, instance):
        suggest_data = set()  # Use a set to avoid duplicates

        # Add base fields to suggest data
        suggest_data.update([instance.name, instance.title, instance.department, instance.university])

        # Parse and add research_areas
        if instance.research_areas and isinstance(instance.research_areas, str):
            research_areas_list = instance.research_areas.split('\n')
            suggest_data.update(research_areas_list)

        # Convert set back to list for Elasticsearch
        return {"input": list(suggest_data), "weight": 1}








# @registry.register_document
# class ProfessorDocument(Document):
#     class Index:
#         name = 'professor_index'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 0, 'max_result_window': 2000000,'analysis': {
#                 'analyzer': {
#                     'default': {
#                         'type': 'custom',
#                         'tokenizer': 'standard',
#                     },
#                 },
#             },}

    


#     @classmethod
#     def update_document(cls, professor_instance):
#         document = cls(meta={'id': professor_instance.id})
#         document.name = professor_instance.name
#         document.title = professor_instance.title
#         document.phone = professor_instance.phone
#         document.address = professor_instance.address
#         document.introduction = professor_instance.introduction
#         document.achievements = professor_instance.achievements
        
#         document.city = professor_instance.city
#         document.province = professor_instance.province
#         document.country = professor_instance.country
#         document.email = professor_instance.email
#         document.research_areas = professor_instance.research_areas
#         document.image_url = professor_instance.image_url
#         document.university = professor_instance.university
#         document.department = professor_instance.department
#         document.save()

#     @classmethod
#     def delete_document(cls, professor_instance):
#         document = cls(meta={'id': professor_instance.id})
#         document.delete(ignore=404)
#     class Django:
#         model = Professor


#     def prepare_suggest(self, instance):
#         suggest_data = set()  # Use a set to avoid duplicates

#         # Add base fields to suggest data
#         suggest_data.update([instance.name, instance.title, instance.department, instance.university])

#         # Parse and add research_areas
#         if instance.research_areas and isinstance(instance.research_areas, str):
#             research_areas_list = instance.research_areas.split('\n')
#             suggest_data.update(research_areas_list)

#         # Convert set back to list for Elasticsearch
#         return {"input": list(suggest_data), "weight": 1}
    

    # def index_document(self, professor_instance):
    #     # Calculate non-empty fields
    #     fields_to_check = [
    #         professor_instance.name,
    #         professor_instance.title,
    #         professor_instance.phone,
    #         professor_instance.address,
    #         professor_instance.introduction,
    #         professor_instance.achievements,
    #         professor_instance.city,
    #         professor_instance.country,
    #         professor_instance.email,
    #         professor_instance.research_areas,
    #         professor_instance.image_url,
    #         professor_instance.university,
    #         professor_instance.department
    #     ]

    #     non_empty_field_count = sum(1 for field in fields_to_check if field)

    #     # Update the non_empty_field_count of the professor_instance
    #     professor_instance.non_empty_field_count = non_empty_field_count
    #     professor_instance.save()