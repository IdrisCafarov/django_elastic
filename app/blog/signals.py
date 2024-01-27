# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .documents import ProfessorDocument
# from .utils import update_elasticsearch_bulk
# from .models import *

# @receiver(post_save, sender=Professor)
# def update_document_on_save(sender, instance, **kwargs):
#     ProfessorDocument.update_document(instance)

# @receiver(post_delete, sender=Professor)
# def delete_document_on_delete(sender, instance, **kwargs):
#     ProfessorDocument.delete_document(instance)



# @receiver(post_save, sender=Professor)
# def update_custom_field(sender, instance, **kwargs):
#     doc_instance = ProfessorDocument(meta={'id': instance.id})
#     doc_instance.non_empty_field_count = instance.get_non_empty_field_count()
#     # non_empty_field_count = instance.get_non_empty_field_count()
#     # non_empty_fields_rating = instance.calculate_non_empty_fields_rating(non_empty_field_count)
#     # university_world_ranking_rating = instance.calculate_university_world_ranking_rating()
#     doc_instance.rating = instance.calculate_rating()

#     doc_instance.save()