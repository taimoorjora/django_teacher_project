from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
import csv, io
from zipfile import ZipFile
from django.core.files.base import File
from django.contrib.auth.decorators import login_required

from teacher.models import Teacher, Subject, TeacherSubject

@login_required(login_url='/accounts/login/')
def data_upload(request):
    if request.method == 'GET':
        return render(request, 'teacher/data_upload.html',{})

    data_file = request.FILES['file']
    images_zip = request.FILES['images']

    if not data_file.name.endswith('.csv') and not images_zip.name.endswith('.zip'):
        messages.error(request, 'This is not a csv file')
        return render(request, 'teacher/data_upload.html',{})

    data_set = data_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)


    zipped_files = ZipFile(images_zip)
    image_names = zipped_files.namelist()


    for column in csv.reader(io_string,  delimiter=',', quotechar='"'):
        if not column[3] == '':
            image_name = column[2]
            teacher, created = Teacher.objects.update_or_create(
                first_name=column[0],
                last_name=column[1],
                email_address=column[3],
                phone_number=column[4],
                room_number=column[5]
            )

            if not image_name == '':
                if image_name in image_names:
                    zip_img = zipped_files.read(image_name)
                    tmp_file = io.BytesIO(zip_img)
                    dummy_file = File(tmp_file)
                    dummy_file.name = image_name
                    dummy_file.size = len(zip_img)
                    dummy_file.file = tmp_file
                    teacher.profile_picture = dummy_file
                    teacher.save()

            subjects = column[6].split(',')
            subjects_taught_count = TeacherSubject.objects.filter(teacher=teacher).count()

            for subject in subjects:
                if subjects_taught_count>5:
                    break
                
                subject = subject.strip().lower()
                subject_object, created = Subject.objects.update_or_create(title=subject)
                TeacherSubject.objects.update_or_create(teacher=teacher, subject=subject_object)
                subjects_taught_count +=1
    
    messages.success(request, 'Data has been uploaded')
    return render(request, 'teacher/data_upload.html',{})