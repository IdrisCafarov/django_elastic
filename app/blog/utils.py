

from .documents import ProfessorDocument
from elasticsearch.helpers import bulk
from django_elasticsearch_dsl import Index


def update_elasticsearch_bulk(model_instances):
    data = [
        {
            '_op_type': 'index',
            '_index': ProfessorDocument.Index.name,
            '_id': str(instance.id),
            '_source': {
                # Map your model fields to Elasticsearch fields
                'name': instance.name,
                'title': instance.title,
                'email': instance.email,
                'research_areas': instance.research_areas,
                'image_url': instance.image_url,
                'university': instance.university,
                'department': instance.department,
                # Add other fields as needed
            }
        }
        for instance in model_instances
    ]

    # Get the Elasticsearch client
    es = Index(ProfessorDocument.Index.name).doc_type(ProfessorDocument).to_es()

    success, failed = bulk(es, data)
    print(f'Successful updates: {success}, Failed updates: {failed}')

def clear_index():
    index = Index(ProfessorDocument.Index.name)
    index.delete(ignore=404)
    index.create()
    index.refresh()
