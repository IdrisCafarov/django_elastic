from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from elasticsearch.helpers import scan
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
import requests
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


# Create your views here.

from django.views import View
from django_elasticsearch_dsl.search import Search
from .models import *
from .forms import *
import json
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponseRedirect
from elasticsearch_dsl import Q, SF
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .helpers import *
from django.db.models import Case, When, Value, IntegerField




#########################   TESTING  #################################

from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    FunctionalSuggesterFilterBackend
    
)
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_EXCLUDE,
)


from .serializers import *

class ProfessorViewSet(DocumentViewSet):
    document = ProfessorDocument
    serializer_class = ProfessorDocumentSerializer
    filter_backends = [FilteringFilterBackend, OrderingFilterBackend, SearchFilterBackend,FunctionalSuggesterFilterBackend]

    # Define filter fields
    filter_fields = {
        'id': {
            'field': '_id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
            ],
        },
      
        'title': {
            'field': 'title',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
                
            ],
        },

        'name': {
            'field': 'name',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },

        
    }

    # Define ordering fields
    ordering_fields = {
        'title': 'title.row',
        'rating': 'rating',
        # 'name': 'name',
        # other ordering fields...
    }

    # Define search fields
    search_fields = {
        'research_areas': {'boost': 1,'fuzziness': 'AUTO'},
        'department': {'boost': 3,'fuzziness': 'AUTO'},
        'name': {'boost': 6,'fuzziness': 'AUTO'},
        'introduction': {'boost': 4},
        'email': {'boost': 7,'fuzziness': 'AUTO'},
        
        # other searchable fields...
    }

    ordering = ('rating',)


    functional_suggester_fields = {
        'suggest': {
            'field': 'suggest',
            'suggesters': ['completion'],
            'options': {
                'size': 5,  # Number of suggestions to return
                'skip_duplicates': True,
                'fuzziness': 1
            }
        }
    }

    
    highlight_fields = {
        'name': {
            'enabled': True,
            'options': {
                'pre_tags': ["<b>"],
                'post_tags': ["</b>"],
            }
        },
    }


    

    def get_queryset(self):
        # Start with the default queryset
        queryset = super().get_queryset()

        # Retrieve additional filter parameters
        selected_universities = self.request.query_params.getlist('universities[]')
        selected_cities = self.request.query_params.getlist('cities[]')
        selected_titles = self.request.query_params.getlist('titles[]')
        
        # search_query = self.request.query_params.get('search', '') 

        # Apply filters for universities
        if selected_universities:
            print(selected_universities)
            university_filters = [Q('term', university=university) for university in selected_universities]
            queryset = queryset.query('bool', should=university_filters)

        # Apply filters for cities
        if selected_cities:
            city_filters = [Q('term', city=city) for city in selected_cities]   
            queryset = queryset.query('bool', should=city_filters)

        # Apply filters for titles
        must_not_filters = []
        exclude_filters = []
        title_list = []
        # Add titles to title_list if they are not in selected_titles
        if "Associate Professor" not in selected_titles:
            title_list.append("Associate Professor")
        if "Assistant Professor" not in selected_titles:
            title_list.append("Assistant Professor")
        if "Adjunct professor" not in selected_titles:
            title_list.append("Adjunct professor")

        # Create filters based on title_list and selected_titles
        exclude_filters = [Q('wildcard', title=f'*{exclude_title}*') for exclude_title in title_list]
        title_filters = [Q('wildcard', title=f'*{title}*') for title in selected_titles]

        # Apply filters to the queryset
        if exclude_filters:
            queryset = queryset.query('bool', must_not=exclude_filters)
        if title_filters:
            queryset = queryset.query('bool', should=title_filters)

            



#         sort_script = {
#     "_script": {
#         "type": "number",
#         "script": {
#             "lang": "painless",
#             "source": """
#             int nonEmptyFields = 0;
#             if (doc['non_empty_field_count'].size() != 0) {
#                 nonEmptyFields = (int) doc['non_empty_field_count'].value;
#             }

#             String title = doc['title'].value;
#             int titlePriority = title.contains('Associate Professor') ? 2 :
#                                 title.contains('Assistant Professor') ? 3 :
#                                 title.contains('Professor') ? 1 :
#                                 title.contains('Lecturer') ? 4 : 99;

#             int orderValue = (nonEmptyFields * -1) + titlePriority;
#             return orderValue;
#             """
#         },
#         "order": "asc"
#     }
# }





        # Apply script-based sorting
        # queryset = queryset.sort(sort_script)
        
        return queryset
    
   
    



class SearchSuggestionView(ViewSet):
    def list(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        suggestions = self.get_search_suggestions(query)
        return Response({'suggestions': suggestions})

    def get_search_suggestions(self, query):
        if not query:
            return []

        search = Search(index='professors')
        search = search.suggest('professor_suggester', query, completion={'field': 'suggest'})
        response = search.execute()

        # Use a set to collect unique suggestions
        suggestions = set()
        for suggestion in response.suggest.professor_suggester[0].options:
            suggestions.add(suggestion.text)

        # Convert the set back to a list for the response
        return list(suggestions)


##########################################################################


from django.conf import settings


@login_required(login_url='/user_login/')
def index(request):
    print(settings.ELASTICSEARCH_INDEX_NAMES)
    # if request.user.is_authenticated and request.user.is_superuser:
    #     print("salam")

    
    

    query = request.GET.get('q', '')

    # Use Elasticsearch DSL to perform the search
    search = Search(index='professors').query('multi_match', query=query, fields=['name^3', 'title^2', 'email', 'research_areas^2'])
    results = search.execute()

    # Access search results
    professors = [hit for hit in results]

    return render(request, 'customer/index.html', {'professors': professors, 'query': query})
























@login_required(login_url='/user_login/')
def search_view(request):
    query = request.GET.get('q', '')

    # Use Elasticsearch DSL to perform the search
    search = Search(index='professor_index').query('multi_match', query=query, fields=['name^3', 'title^2', 'email', 'research_areas^2'])
    results = search.execute()

    # Access search results
    professors = [hit for hit in results]

    return render(request, 'customer/search_result.html', {'professors': professors, 'query': query})






















@login_required(login_url='/user_login/')
def main_search(request):

    context={}

    search = Search(index="professors")

    universities = set(hit.university for hit in search.scan() if hit.university != '')
    cities = set(hit.city for hit in search.scan() if hit.city != '')
    context["universities"] = universities
    context["cities"] = cities
    
    query = request.GET.get('q', '')
    page = request.GET.get('page',1)
    selected_universities = request.GET.getlist('universities[]')
    selected_cities = request.GET.getlist('cities[]')
    selected_titles = request.GET.getlist('titles[]')

    api_url = f'http://127.0.0.1:8000/api/professors/?ordering=-rating&'

    if query:
        api_url += f'search={query}&'

    if page:
        api_url += f'page={page}&'

    if selected_universities:
        # Add multiple universities to the URL
        for university in selected_universities:
            api_url += f'universities[]={university}&'

    if selected_cities:
        # Add multiple cities to the URL
        for city in selected_cities:
            api_url += f'cities[]={city}&'

    if selected_titles:
        # Add multiple cities to the URL
        for title in selected_titles:
            api_url += f'titles[]={title}&'



    response = requests.get(api_url)
    print(api_url)


    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # print(data)
        professors = data.get('results', [])
        next_page = data.get('next')
        previous_page = data.get('previous')
        total_data_count = data.get('count', 0)
        items_per_page = 10
        total_pages = (total_data_count + items_per_page - 1) // items_per_page
       
    else:
        # Handle the case where the API request fails
        professors = []


    

    context["professors"] = professors
    context["query"] = query
    

    if request.is_ajax():
        # If it's an AJAX request, return JSON response
        html = render_to_string("customer/filtered_professors.html", {"professors": professors})

        # Create a data dictionary with the HTML content
        data_dict = {
            "html_from_view": html,
            "next_page": next_page,
            "previous_page": previous_page,
            "totalPages": total_pages,
            "currentPage": page,
        }

        # Return the HTML content as JSON response
        return JsonResponse(data=data_dict, safe=False)
   

    

    return render(request, 'customer/main_search.html', context)




















@login_required(login_url='/user_login/')
def upload_json(request):
    if request.method == 'POST':
        form = JSONFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded JSON file
            json_file = request.FILES['json_file']
            decoded_data = json_file.read().decode('utf-8')
            data = json.loads(decoded_data)

            # Save the data to the database
            for item in data:
                try:
                    Professor.objects.create(
                        name=item.get('name', ''),
                        introduction=item.get('introduction', ''),
                        phone=item.get('phone', ''),
                        address=item.get('address', ''),
                        achievements=item.get('achievements', ''),
                        url=item.get('url', ''),
                        city=item.get('city', ''),
                        province=item.get('province', ''),
                        country="US",
                        title=item.get('title', ''),
                        email=item.get('email', ''),
                        image_url=item.get('photo', ''),
                        research_areas=item.get('direction', ''),
                        university=item.get('school', ''),
                        department=item.get('college', ''),
                        university_world_ranking=324
                    )
                except IntegrityError as e:
                    # Catch unique constraint violation (IntegrityError) and log it
                    print(f"IntegrityError: {e}")
                    # Optionally, you can skip the current iteration and continue with the next one
                    continue
            messages.success(request,'Congratulations,you successfully uploaded data !')
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request,'There is a problem please try again later !')
    else:
        form = JSONFileUploadForm()

    return render(request, 'customer/upload_json.html', {'form': form})




import ast

@login_required(login_url='/user_login/')
def prof_detail(request,slug):
    context={}
    prof = get_object_or_404(Professor,slug=slug)
    context["prof"] = prof
    
    research_list = []
    # Convert the string to a Python list using ast.literal_eval
    if prof.research_areas:
        
        try:
            research_list = prof.research_areas.split('\n')
            # print(research_list)
        except ValueError as e:
            print(f"Error: {e}")

    context["research_list"] = research_list

    print("saalam")

    # professors = Professor.objects.all()
    for professor_instance in Professor.objects.all():
        count = professor_instance.get_non_empty_field_count()
        print("      \n")
        print(f"Instance {professor_instance.id}: Non-empty field count - {count}")

    
    return render(request,"customer/prof_detail.html",context)
    