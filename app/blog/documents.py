# search_indexes.py
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Professor
import ast

# from django_elasticsearch_dsl.fields import ObjectField, URLField


@registry.register_document
class ProfessorDocument(Document):
    class Index:
        name = 'professor_index'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0, 'max_result_window': 2000000}

    name = fields.TextField()
    title = fields.TextField()
    phone = fields.TextField()
    address = fields.TextField()
    introduction = fields.TextField()
    achievements = fields.TextField()
    city = fields.KeywordField()
    province = fields.TextField()
    country = fields.TextField()
    email = fields.TextField()
    research_areas = fields.TextField()
    image_url = fields.TextField()
    university = fields.KeywordField()
    department = fields.TextField()
    # Add the 'slug' field without indexing it
    slug = fields.KeywordField(index=False, store=True)

    suggest = fields.CompletionField()

    


    @classmethod
    def update_document(cls, professor_instance):
        document = cls(meta={'id': professor_instance.id})
        document.name = professor_instance.name
        document.title = professor_instance.title
        document.phone = professor_instance.phone
        document.address = professor_instance.address
        document.introduction = professor_instance.introduction
        document.achievements = professor_instance.achievements
        
        document.city = professor_instance.city
        document.province = professor_instance.province
        document.country = professor_instance.country
        document.email = professor_instance.email
        document.research_areas = professor_instance.research_areas
        document.image_url = professor_instance.image_url
        document.university = professor_instance.university
        document.department = professor_instance.department
        document.save()

    @classmethod
    def delete_document(cls, professor_instance):
        document = cls(meta={'id': professor_instance.id})
        document.delete(ignore=404)
    class Django:
        model = Professor


    def prepare_suggest(self, instance):
        suggest_data = set()  # Use a set to avoid duplicates

        # Add base fields to suggest data
        suggest_data.update([instance.name, instance.title, instance.department, instance.university])

        # Parse and add research_areas
        if instance.research_areas and isinstance(instance.research_areas, str):
            try:
                research_areas_list = ast.literal_eval(instance.research_areas)
                if isinstance(research_areas_list, list):
                    suggest_data.update(research_areas_list)
            except (ValueError, SyntaxError):
                # Handle invalid literal
                pass

        # Convert set back to list for Elasticsearch
        return {"input": list(suggest_data), "weight": 1}


    
