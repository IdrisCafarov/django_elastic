from django.urls import path
from .views import *


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfessorViewSet

router = DefaultRouter()
router.register(r'professors', ProfessorViewSet, basename='professors')
router.register(r'search-suggestions', SearchSuggestionView, basename='search-suggestions'),



# router = DefaultRouter()



urlpatterns = [
    path('api/', include(router.urls)),
]


urlpatterns = [
    path('',index,name="index"),
    path('api/', include(router.urls)),
    path('search/', search_view, name='search'),
    path('main_search/',main_search,name="main_search"),
    # path('upload_json/',upload_json,name="upload_json"),
    # path('search/suggestions/', SearchSuggestionView.as_view(), name='search_suggestions'),
    path('prof_detail/<slug>/',prof_detail,name="prof_detail"),
    path('test/',test,name="test"),

    
]
