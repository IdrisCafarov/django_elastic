from rest_framework import serializers

class JSONFilesUploadSerializer(serializers.Serializer):
    json_files = serializers.ListField(
                   child=serializers.FileField(max_length=100000),
                   allow_empty=False
               )