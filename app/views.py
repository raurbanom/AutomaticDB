# coding=utf-8
import json
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render


# Create your views here.
def base(request):
    return render(request, 'base.html')


def home(request):
    return render(request, 'home.html')


def upload(request):
    # file = request.cleaned_data['file']

    if request.method == 'POST' and (request.FILES and request.FILES['jsonFile']):
        json_file = request.FILES['jsonFile']

        if validate_file_type(json_file):
            fs = FileSystemStorage()

            filename = fs.save(json_file.name, json_file)
            uploaded_file_url = fs.url(filename)

            # Check file
            # process_file(json_file)
            data = process_file(filename)

            if len(data) > 0:
                return render(request, 'upload.html', {
                    'uploaded_file_url': uploaded_file_url,
                    'uploaded_file_data': data
                })
            else:
                return render(request, 'upload.html', {
                    'uploaded_file_message': "No se pudo procesar el archivo. Por favor, intente nuevamente"
                })
        else:
            return render(request, 'upload.html', {
                'uploaded_file_message': "Tipo de archivo no válido. Por favor, intente nuevamente."
            })

    return render(request, 'upload.html')


def manual(request):
    return render(request, 'manual.html')


def about(request):
    return render(request, 'about.html')

# class AboutView(generic.TemplateView):
#     template_name = "about.html"


def get_extension(filename):
    file_type = filename.content_type.split('/')[1]
    print(file_type)

    return file_type

"""
def clean_file(file):
    try:
        if file:
            file_type = file.content_type.split('/')[0]
            print(file_type)

            if len(file.name.split('.')) == 1:
                return False # _('File type is not supported')

            if file_type in settings.VALID_FILE_MIMETYPES:
                return  True
            else:
                return False # _('File type is not supported')
    except:
        pass

    return file
"""


def get_mimetype(json_file):
    ext = os.path.splitext(json_file.name)[1]

    return ext.lower()


def validate_file_type(json_file):
    # noinspection PyBroadException
    try:
        content_type = get_mimetype(json_file)
        if content_type in settings.VALID_FILE_EXTENSION:
            return True
        else:
            return False
    except Exception as ex:
        print(ex.message)
        return False


def process_file(filename):
    path = os.path.join(settings.MEDIA_ROOT, filename)
    # print(path)

    # Read file
    f = open(path)
    json_string = f.read()
    f.close()

    # Convert json string to python object
    # data = json.loads(json_string)

    """json_object = json.load(json_string)  # deserialize it
    json_string = json.dumps(json_data)  # json formatted string
    json_data.close()"""

    return json_string
