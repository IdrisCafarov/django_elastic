from django.urls import path
from .views import *





urlpatterns = [
    path('user_login/',user_login,name="user_login"),
    path('logout/',logout_view, name="user_logout"),
    path('check_session/',check_session,name="check_session"),
    path('dashboard/',dashboard,name="dashboard"),
    path('dashboard_professors/',professors,name="dashboard_professors"),
    path('upload_json/',upload_json,name="upload_json"),
    path('dashboard_professor_detail/<slug>/',professor_detail,name="dashboard_professor_detail"),
    path('dashboard_add_professor/',professor_update,name="dashboard_add_professor"),
    path('dashboard_update_professor/<slug>/',professor_update,name="dashboard_update_professor")
    # path('api/upload-json/', JSONFilesUploadView.as_view(), name='upload_json_files_api'),
    # path('upload/', file_upload,name="file_upload"),
]
