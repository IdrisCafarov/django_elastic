from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from .forms import *

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django_elasticsearch_dsl.search import Search
import requests
from django.template.loader import render_to_string
from blog.models import *


import random
import string


def check_is_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
def check_session(request):
    # This will return HTTP 200 if the session is valid, or redirect to login otherwise
    return JsonResponse({"session": "active"})

def code_slug_generator(size=12, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def create_slug_shortcode(size, model_):
    new_code = code_slug_generator(size=size)
    qs_exists = model_.objects.filter(slug=new_code).exists()
    return create_slug_shortcode(size, model_) if qs_exists else new_code


# Create your views here.


def user_login(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == 'POST':
        print("post")
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            print("valid")
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            login(request, user)
            # request.session.set_expiry(20)

            return redirect(request.GET.get('next', 'index'))

    else:
        form = LoginForm()
    context["form"] = form
    context["next"] = request.GET.get('next', '')
    return render(request,"customer/login.html",context)



def logout_view(request):

    logout(request)
    return redirect('user_login')








@login_required(login_url='/user_login/')
@user_passes_test(check_is_admin)
def dashboard(request):
    return render(request,"dashboard/index.html")



@login_required(login_url='/user_login/')
@user_passes_test(check_is_admin)
def professors(request):
    context={}

    search = Search(index="professor_index")

    universities = set(hit.university for hit in search.scan() if hit.university != '')
    cities = set(hit.city for hit in search.scan() if hit.city != '')
    titles = Title.objects.all()
    context["universities"] = universities
    context["cities"] = cities
    context["titles"] = titles
    
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
        html = render_to_string("dashboard/filtered_professors.html", {"professors": professors})

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
   
    return render(request,"dashboard/professors.html",context)



def upload_json(request):
    

    return render(request,"dashboard/upload_json.html")


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JSONFileUploadSerializer
import json

class JSONFilesUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = JSONFilesUploadSerializer(data=request.data)

        if serializer.is_valid():
            files = serializer.validated_data['json_files']

            for file in files:
                decoded_data = file.read().decode('utf-8')
                data = json.loads(decoded_data)
                # Process each JSON file here

            return Response({"message": "Files uploaded successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)