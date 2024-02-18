from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import HttpResponseRedirect
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

    search = Search(index="professors")

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
    selected_tab = request.GET.get('tab', '')

    api_url = f'http://127.0.0.1:8000/api/professors/?ordering=-rating&'

    if query:
        api_url += f'search={query}&'

    

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


    api_url_2 = api_url + 'public=false'
    response_non_public = requests.get(api_url_2)

    api_url_3 = api_url + 'public=true'
    response_public = requests.get(api_url_3)

    if page:
        api_url += f'page={page}&'

    


    

    if selected_tab:
        if selected_tab == 'published':
            api_url += 'public=true&'
        elif selected_tab == 'draft':
            api_url += 'public=false&'
        # api_url += f'selected_tab={selected_tab}&'


    print(api_url)
    response = requests.get(api_url)
    

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        data_2 = response_non_public.json()
        data_3 = response_public.json()
        total_non_public = data_2.get('count', 0)
        
        # print(data)
        professors = data.get('results', [])
        next_page = data.get('next')
        previous_page = data.get('previous')
        total_data_count = data.get('count', 0)
        total_public_count = data_3.get('count', 0)
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
            "totalCount": total_non_public + total_public_count,
            "totalNonPublicCount": total_non_public,
            "totalPublicCount": total_public_count
        }

        # Return the HTML content as JSON response
        return JsonResponse(data=data_dict, safe=False)
   
    return render(request,"dashboard/professors.html",context)

@login_required(login_url='/user_login/')
def professor_detail(request,slug):
    context = {}
    professor = get_object_or_404(Professor,slug=slug)
    research_list = []
    # Convert the string to a Python list using ast.literal_eval
    if professor.research_areas:
        
        try:
            research_list = professor.research_areas.split('\n')
            # print(research_list)
        except ValueError as e:
            print(f"Error: {e}")

    context["research_list"] = research_list

    context["professor"] = professor




    return render(request,"dashboard/professor_detail.html",context)


def professor_update(request,slug=None):
    # Check if the pk is provided, if yes, then it's an update operation
    instance = get_object_or_404(Professor, slug=slug) if slug else None
    
    if request.method == 'POST':
        print("indisde methdo")
        form = UpdateDataForm(request.POST, instance=instance)
        if form.is_valid():
            print("inside valiud")
            form.save()
            if slug:
                messages.success(request,'Succesfully Updated')
            else:
                messages.success(request,'Succesfully Added')
            return redirect('dashboard_professors')
        else:
            messages.error(request,'Error occured while handling')
    else:
        form = UpdateDataForm(instance=instance)
    
    return render(request, 'dashboard/add_professor.html', {'form': form})








def upload_json(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('file')
        data_to_send = []
        
          
        for uploaded_file in uploaded_files:
            try:
                # Process the uploaded JSON file
                decoded_data = uploaded_file.read().decode('utf-8')
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
                    data_to_send.append(item)
                    print(data_to_send)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        # Return success response
        return JsonResponse({'message': 'Data uploaded successfully!','data': data_to_send})
    
    
    return render(request, 'dashboard/upload_json.html')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .serializers import JSONFileUploadSerializer
import json

# class JSONFilesUploadView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = JSONFilesUploadSerializer(data=request.data)

#         if serializer.is_valid():
#             files = serializer.validated_data['json_files']

#             for file in files:
#                 decoded_data = file.read().decode('utf-8')
#                 data = json.loads(decoded_data)
#                 # Process each JSON file here

#             return Response({"message": "Files uploaded successfully!"}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)