from django.urls import path
from teacher import views as view

app_name='teacher'

urlpatterns = [
    path('', view.teacher_list, name="teacherlist"),
    path('<int:id>/', view.teacher_detail, name="teacherdetail"),
    path('uploader/', view.data_upload, name="dataupload"),

]