from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .documents import ProfessorDocument
from .utils import update_elasticsearch_bulk
from .models import *

@receiver(post_save, sender=Professor)
def update_document_on_save(sender, instance, **kwargs):
    ProfessorDocument.update_document(instance)

@receiver(post_delete, sender=Professor)
def delete_document_on_delete(sender, instance, **kwargs):
    ProfessorDocument.delete_document(instance)