from django.urls import path
from .views import *

urlpatterns = [
    path('user_login/',user_login,name="user_login"),
    path('logout/',logout_view, name="user_logout"),
    path('check_session/',check_session,name="check_session"),
    path('dashboard/',dashboard,name="dashboard"),
    path('dashboard_professors/',professors,name="dashboard_professors"),
    path('upload_json/',upload_json,name="upload_json"),
    path('api/upload-json/', JSONFilesUploadView.as_view(), name='upload_json_files_api'),
    # path('upload/', file_upload,name="file_upload"),
]
