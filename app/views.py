# coding=utf-8
import json
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from RecubrimientoMinimo import RecubrimientoMinimo


def base(request):
    return render(request, 'base.html')


def home(request):
    return render(request, 'home.html')


def result(request):
    return render(request, 'result.html')


def upload(request):
    active = False

    if request.POST:
        if 'btnUpload' in request.POST:
            if request.method == 'POST' and (request.FILES and request.FILES['fileJson']):
                response = upload_json(request)
            else:
                response = {
                    "uploaded_file_message": "Archivo JSON es requerido. Por favor, intente nuevamente."
                }

            # if "uploaded_file_active" in response:
            #     print("uploaded_file_active" + str(response['uploaded_file_active']))

            return render(request, "upload.html", response)

    return render(request, "upload.html")


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


# ----------------------------------------
# -
# -------------------------------------------

# ------------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------------

def upload_json(request):
    if request.FILES and request.FILES['fileJson']:
        json_file = request.FILES['fileJson']

        if validate_file_type(json_file):
            fs = FileSystemStorage()

            filename = fs.save(json_file.name, json_file)
            uploaded_file_url = fs.url(filename)

            # Check file
            if is_json(filename):
                # data = process_file(filename)
                path = os.path.join(settings.MEDIA_ROOT, filename)

                recubrimiento = RecubrimientoMinimo(path)
                recubrimiento.get_descomposicion()

                data = recubrimiento.get_operaciones_L0()
                data += recubrimiento.print_descomposicion()
            else:
                data = ""

            if len(data) > 0:
                return {
                    "uploaded_file_url": uploaded_file_url,
                    "uploaded_file_data": data
                }
            else:
                return {
                    "uploaded_file_message": "No se pudo procesar el archivo. Por favor, intente nuevamente"
                }
        else:
            return {
                "uploaded_file_message": "Tipo de archivo no válido. Por favor, intente nuevamente"
            }


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
    json_string = get_file_text(filename)
    return json_string


def get_file_text(filename):
    path = os.path.join(settings.MEDIA_ROOT, filename)

    # file_io = open(path, encoding='utf-8'))
    file_io = open(path, 'r')
    text = file_io.read().decode('utf-8')
    file_io.close()

    return text


def is_json(filename):
    # noinspection PyBroadException
    try:
        text_data = get_file_text(filename)
        json.loads(text_data)

        # j = text_data
        # j = re.sub(r"{\s*(\w)", r'{"\1', j)
        # j = re.sub(r",\s*(\w)", r',"\1', j)
        # j = re.sub(r"(\w):", r'\1":', j)
    except Exception as ex:
        return False
    return True
