from django.shortcuts import render

# Create your views here.

from django.views import View
from django_elasticsearch_dsl.search import Search
from .models import *

def search_view(request):
    template_name = 'search_result.html'

    query = request.GET.get('q', '')

    if query:
        search = Search(index='posts').query(
        'multi_match', 
        query=query, 
        fields=['title^3', 'content'],
        fuzziness='AUTO'  # Add this line for fuzzy matching
    )
        results = search.execute()

    else:
        results = []

    return render(request, template_name, {'query':query, 'results':results})
