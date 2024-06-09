from upload_file.models import UploadedFile
from rest_framework import serializers


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'