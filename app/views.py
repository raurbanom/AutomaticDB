# coding=utf-8
from __future__ import division

import json
import os
from datetime import datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from AutomaticDB.settings import MEDIA_URL
from RecubrimientoMinimo import RecubrimientoMinimo

error_messages = {
    'file_required': "Archivo JSON es requerido. Por favor, intente nuevamente.",
    'file_process': "No se pudo procesar el archivo. Por favor, intente nuevamente",
    'file_type': "Tipo de archivo no válido. Por favor, intente nuevamente",
}


def base(request):
    return render(request, 'base.html')


def home(request):
    return render(request, 'home.html')


def upload(request):
    if request.POST:
        if 'btnUpload' in request.POST:
            if request.method == 'POST' and (request.FILES and request.FILES['fileJson']):
                response = upload_json(request)
            else:
                response = {
                    "uploaded_file_message": error_messages["file_required"]
                }

            return render(request, "upload.html", response)

    return render(request, "upload.html")


def create_json(attributes, dependencies):
    try:
        # Perform data
        dependencies_temp = dependencies.replace(" ", "")
        list_attributes = attributes.replace(" ", "").split(",")
        list_dependencies = dependencies_temp.split(";")

        # Parse data
        result = []
        for pair in list_dependencies:
            x, y = pair.split(":")
            result.append({"x": x, "y": y})

        data = {
            "attributes": list_attributes,
            "functionaldependencies": result
        }

        # format data
        json_data = json.dumps(data, indent=4)

        filename = get_file_name(".json")
        result = create_file(filename, json_data)

        if result:
            return {
                "uploaded_file_url": filename
            }
        else:
            return {
                "uploaded_file_message": error_messages["file_process"]
            }
    except:
        return {
            "uploaded_file_message": error_messages["file_process"]
        }


def manual(request):
    if request.POST and 'btnProcess' in request.POST:
        # return redirect(reverse('home'))
        attributes = request.POST.get('txtAttributes', '')
        dependencies = request.POST.get('txtDependencies', '')

        print(attributes)
        print(dependencies)

        result = create_json(attributes, dependencies)

        if "uploaded_file_url" in result:
            filename = result["uploaded_file_url"]
            uploaded_file_url = MEDIA_URL + filename

            # Check file
            if is_json(filename):
                path = os.path.join(settings.MEDIA_ROOT, filename)
                data, log = get_minimal_closure(path)
                upload_file_data = MEDIA_URL + log
            else:
                data = ""
                upload_file_data = ""

            result = {
                "uploaded_file_url": uploaded_file_url,
                "uploaded_file_log": upload_file_data,
                "uploaded_file_data": data
            }

        return render(request, 'manual.html', result)

    return render(request, 'manual.html')


def about(request):
    return render(request, 'about.html')


def get_extension(filename):
    file_type = filename.content_type.split('/')[1]
    print(file_type)

    return file_type


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
                path = os.path.join(settings.MEDIA_ROOT, filename)
                data, log = get_minimal_closure(path)
                upload_file_data = MEDIA_URL + log
            else:
                data = ""
                upload_file_data = ""

            if len(data) > 0:
                return {
                    "uploaded_file_url": uploaded_file_url,
                    "uploaded_file_log": upload_file_data,
                    "uploaded_file_data": data
                }
            else:
                return {
                    "uploaded_file_message": error_messages["file_process"]
                }
        else:
            return {
                "uploaded_file_message": error_messages["file_type"]
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



def get_file_name(extension):
    now = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    td = now - epoch

    return 'file_' + str(int(round(td.total_seconds()))) + str(extension)


def create_file(filename, data):
    try:

        path = os.path.join(settings.MEDIA_ROOT, filename)

        # Create file
        file_io = open(path, 'w+')
        file_io.write(data)
        file_io.close()
        return True
    except:
        return False


def get_minimal_closure(path):
    try:
        recubrimiento = RecubrimientoMinimo(path)
        list_final, txt_data = recubrimiento.get_resultado()

        filename = get_file_name(".txt")
        result = create_file(filename, txt_data)

        if result:
            return list_final, filename
        else:
            return "", ""
    except:
        return "", ""
