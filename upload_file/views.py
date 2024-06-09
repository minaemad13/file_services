import os
import random
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from upload_file.serializer import FileSerializer
from upload_file.models import UploadedFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from collections import Counter


# # Create your views here.

# # def upload (request):
# #     if request.method == 'GET':
# #         # data = request.body
# #         # print(data)
# #         return render(request,'file_upload/upload.html')
# #     else:
# #         if request.FILES['file'] :
# #             file_uploaded = UploadedFile.objects.create(filename=request.POST['file_name'], file=request.FILES['file'])
# #             context = {'fileName': request.POST['file_name'],'id':file_uploaded.id}
# #         print(request.headers.get('Accept', ''))
# #         return render(request,'file_upload/upload.html',context)


def get_most_common_letter(line):
    line = "".join(filter(str.isalpha, line)).lower()
    if not line:
        return None
    counter = Counter(line)
    most_common_letter = counter.most_common(1)[0][0]
    return most_common_letter


def get_random_line(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    if not lines:
        return HttpResponse("The file is empty.", status=204)

    random_line = random.choice(lines).strip()
    line_number = lines.index(random_line + "\n") + 1

    return random_line, line_number


@api_view(["POST"])
def upload(request):

    file_serializer = FileSerializer(data=request.data)

    if file_serializer.is_valid():
        file_serializer.save()
        uploaded_file_instance = UploadedFile.objects.get(id=file_serializer.data["id"])
        context = {
            "id": file_serializer.data["id"],
            "filename": uploaded_file_instance.fileName(),
        }
        return Response({"result": context}, status=200)
    else:
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_one_random_line(request):
    uploaded_files = UploadedFile.objects.all()

    random_file = random.choice(uploaded_files)
    file_path = random_file.file.path
    if not random_file:
        return HttpResponse("The file path is missing.", status=400)

    if not os.path.exists(file_path):
        return HttpResponse("The file does not exist.", status=404)

    try:
        random_line, line_number = get_random_line(file_path)

        most_common_letter = get_most_common_letter(random_line)

        accept_header = request.headers.get("Accept", "text/plain")

        if accept_header == "application/json":
            response_data = {"line": random_line}
            return JsonResponse(response_data)

        elif accept_header == "application/xml":
            response_data = f"<response><line>{random_line}</line></response>"
            return HttpResponse(response_data, content_type="application/xml")

        elif accept_header.startswith("application/*"):
            response_data = {
                "line_number": line_number,
                "file_name": os.path.basename(file_path),
                "most_common_letter": most_common_letter,
                "line": random_line,
            }
            return JsonResponse(response_data)

        else:
            return HttpResponse(random_line, content_type="text/plain")
    except FileNotFoundError:
        return HttpResponse("The file does not exist.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


@api_view(["GET"])
def get_one_random_line_backword(request):
    uploaded_files = UploadedFile.objects.all()

    random_file = random.choice(uploaded_files)
    file_path = random_file.file.path
    if not random_file:
        return HttpResponse("The file path is missing.", status=400)

    if not os.path.exists(file_path):
        return HttpResponse("The file does not exist.", status=404)

    try:
        random_line, line_number = get_random_line(file_path)

        response_data = {
            "line_backword": random_line[::-1],
            "line_number": line_number,
        }
        return JsonResponse(response_data)
    except FileNotFoundError:
        return HttpResponse("The file does not exist.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

@api_view(['GET'])
def longest_100_lines(request):
    all_lines = []
    for uploaded_file in UploadedFile.objects.all():
        with open(uploaded_file.file.path, 'r') as f:
            all_lines.extend(f.readlines())
            
            
    longest_lines = sorted(all_lines, key=len, reverse=True)[:100]
    response_data = {
            "longest_100_line": longest_lines,
        }
    return JsonResponse(response_data)

@api_view(["GET"])
def longest_20_lines(request):
    all_lines=[]
    uploaded_files = UploadedFile.objects.all()

    random_file = random.choice(uploaded_files)
    file_path = random_file.file.path
    if not random_file:
        return HttpResponse("The file path is missing.", status=400)

    if not os.path.exists(file_path):
        return HttpResponse("The file does not exist.", status=404)

    try:
        with open(file_path, 'r') as f:
            all_lines.extend(f.readlines())

        longest_lines = sorted(all_lines, key=len, reverse=True)[:20]
        response_data = {
            "longest_20_line":longest_lines
        }
        return JsonResponse(response_data)
    except FileNotFoundError:
        return HttpResponse("The file does not exist.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)