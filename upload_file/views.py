import os
import random
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from upload_file.serializer import FileSerializer
from upload_file.models import UploadedFile
import heapq
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
     # Retrieve all uploaded files
    uploaded_files = UploadedFile.objects.all()

    # Select a random file from the uploaded files
    selected_file = random.choice(uploaded_files)
    file_path = selected_file.file.path

    # Check if the selected file exists
    if not os.path.exists(file_path):
        return HttpResponse("The file does not exist.", status=404)
    
    try:
        # Retrieve a random line from the selected file
        random_line, line_number = get_random_line(file_path)
        
        # Determine the most common letter in the random line
        most_common_letter = get_most_common_letter(random_line)
        
        # Get the 'Accept' header from the request
        accept_header = request.headers.get("Accept", "text/plain")

        # Return the response in the format specified by the 'Accept' header
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
        return HttpResponse(f"An error occurred: {str(e)}", status=400)


@api_view(["GET"])
def get_one_random_line_backword(request):
    # Get all uploaded files
    uploaded_files = UploadedFile.objects.all()
    # Check if there are any uploaded files
    if not uploaded_files:
        return HttpResponse("No uploaded files found.", status=400)
    # Get Path of random file 
    file = random.choice(uploaded_files)
    file_path = file.file.path
    # Check if file exists 
    if not os.path.exists(file_path):
        return HttpResponse("The file does not exist.", status=400)
    
    try:
        #get random line and line number from the random file 
        random_line, line_number = get_random_line(file_path)
        
        response_data = {
            "line_backword": random_line[::-1],
            "line_number": line_number,
            'file_name': file.fileName()
        }
        return JsonResponse(response_data)
    except FileNotFoundError:
        return HttpResponse("The file does not exist.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=400)



@api_view(["GET"])
def get_requested_backword(request):
    # Get all uploaded files
    uploaded_files = UploadedFile.objects.all()

    # Retrieve line number from request, default to 0 if not provided
    line_number = int(request.data.get('line_number', 0))

    # Check if there are any uploaded files
    if not uploaded_files:
        return HttpResponse("No uploaded files found.", status=400)

    # Select a random file from the uploaded files
    random_file = random.choice(uploaded_files)
    file_path = random_file.file.path

    # Check if the file path is missing
    if not file_path:
        return HttpResponse("The file path is missing.", status=400)

    # Check if the file exists
    if not os.path.exists(file_path):
        return HttpResponse("The file does not exist.", status=404)

    try:
        # Check if the line number is valid
        if line_number > 0:
            with open(file_path, 'r') as file:
                # Iterate through the file line by line
                for current_line_number, line in enumerate(file, start=1):
                    # If the current line number matches the requested line number
                    if current_line_number == line_number:
                        # Reverse the line and prepare the response data
                        line_reversed = line.strip()[::-1]
                        response_data = {"line_backward": line_reversed, "line_number": line_number,'file_name':random_file.fileName()}
                        return JsonResponse(response_data)
            # If the file doesn't contain the requested line number
            return HttpResponse(f"The file does not contain line number: {line_number}", status=400)
        else:
            # If the line number is not greater than 0
            return HttpResponse("Please enter a line number greater than 0.", status=400)
    except FileNotFoundError:
        return HttpResponse("The file does not exist.", status=404)
    except Exception as e:
        # Catch any other exceptions and return an error message
        return HttpResponse(f"An error occurred: {str(e)}", status=500)



@api_view(['GET'])
def longest_100_lines(request):
    all_lines = []
    # Iterate through each uploaded file
    for uploaded_file in UploadedFile.objects.all():
        # Open the file and read all lines
        with open(uploaded_file.file.path, 'r') as f:
            # Extend the all_lines list with lines from the current file
            all_lines.extend(f.readlines())

    # Sort all_lines based on line length in descending order and select the top 100 longest lines
    longest_lines = sorted(all_lines, key=len, reverse=True)[:100]

    response_data = {
            "longest_100_line": longest_lines,
        }
    return JsonResponse(response_data)
    
@api_view(["GET"])
def longest_20_lines(request):
    all_lines=[]
    
    # Fetch all uploaded files
    uploaded_files = UploadedFile.objects.all()
    
    # Select a random file from the uploaded files
    random_file = random.choice(uploaded_files)
    
    # Get the file path of the randomly selected file
    file_path = random_file.file.path
    
    # Check if the randomly selected file exists
    if not random_file:
        return HttpResponse("The file path is missing.", status=400)

    # Check if the file exists in the system
    if not os.path.exists(file_path):
        return HttpResponse("The file does not exist.", status=404)

    try:
        # Open the file and read all lines
        with open(file_path, 'r') as f:
            # Extend the all_lines list with lines from the file
            all_lines.extend(f.readlines())

        # Sort all_lines based on line length in descending order and select the top 20 longest lines
        longest_lines = sorted(all_lines, key=len, reverse=True)[:20]
        
        # Prepare response data with the top 20 longest lines
        response_data = {
            "longest_20_line": longest_lines
        }
        
        # Return JSON response containing the top 20 longest lines
        return JsonResponse(response_data)
    
    except FileNotFoundError:
        # Return error response if the file does not exist
        return HttpResponse("The file does not exist.", status=404)
    
    except Exception as e:
        # Return error response for any other exceptions
        return HttpResponse(f"An error occurred: {str(e)}", status=500)