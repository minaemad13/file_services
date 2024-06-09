from django.contrib import admin
from django.urls import path

from upload_file.views import get_one_random_line, get_one_random_line_backword, longest_100_lines, longest_20_lines, upload

urlpatterns = [
    path('upload/', upload),
    path('get_one_random_line/', get_one_random_line),
    path('get_one_random_line_backword/', get_one_random_line_backword),
    path('get_longest_100_lines/', longest_100_lines),
    path('get_longest_20_lines/', longest_20_lines),
]
