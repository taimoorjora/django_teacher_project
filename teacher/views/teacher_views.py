from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
import csv, io
from zipfile import ZipFile
from django.core.files.base import File
from django.contrib.auth.decorators import login_required

from .models import Teacher, Subject, TeacherSubject


def teacher_list(request):
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()

    if request.method == 'GET':
        first_letter = request.GET.get('fletter')
        subject = request.GET.get('subject')

        if first_letter or subject:
            if first_letter:
                teachers = teachers.filter(last_name__istartswith=first_letter[0])
            elif subject:
                teachers = teachers.select_related()
                teachers = teachers.filter(subject_taught__subject__pk=subject).distinct()
                
    context = {
        'subjects': subjects,
        'teachers': teachers
    }

    return render(request, 'teacher/teacher_list.html', context)


def teacher_detail(request, id):
    teacher = Teacher.objects.get(pk=id)
    subject_taught = TeacherSubject.objects.filter(teacher=teacher)
    context = {
        'teacher': teacher,
        'subject_taught':subject_taught
    }

    return render(request, 'teacher/teacher_detail.html', context)
