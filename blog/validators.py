import os
from django.core.exceptions import ValidationError


def validate_pdf(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_video(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mkv', '.amv', '.mp4', '.m4v', '.m4p']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
