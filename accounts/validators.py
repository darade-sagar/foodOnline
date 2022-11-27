from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]
    valid_extension = ['.png','.jpg','.jpeg']

    if  ext.lower() not in valid_extension:
        raise ValidationError(f"Unsupported file extension '{ext}'. Allowed Extensions : {str(valid_extension)}")