# # update_elasticsearch.py

# from django.core.management.base import BaseCommand
# from elasticsearch.helpers import bulk
# from blog.documents import ProfessorDocument
# from blog.models import Professor  # Import your model

# class Command(BaseCommand):
#     help = 'Update Elasticsearch index'

#     def handle(self, *args, **options):
#         # Get all instances of your model
#         model_instances = Professor.objects.all()

#         # Get the Elasticsearch client
#         es = ProfessorDocument._doc_type.index.to_es()

#         # Create a list of actions for bulk update
#         data = [
#             {
#                 '_op_type': 'index',
#                 '_index': ProfessorDocument._doc_type.index,
#                 '_id': str(instance.id),  # Assuming 'id' is the primary key of your model
#                 '_source': ProfessorDocument(instance).to_dict(include_meta=True),
#             }
#             for instance in model_instances
#         ]

#         # Perform bulk update
#         success, failed = bulk(es, data)

#         self.stdout.write(self.style.SUCCESS('Successfully updated Elasticsearch index'))
