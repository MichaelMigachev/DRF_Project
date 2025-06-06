from rest_framework.serializers import ValidationError

# not_forbidden = "https://www.youtube.com/"
not_forbidden = "www.youtube.com"


def validate_not_forbidden(value):
    if not_forbidden not in value:
        raise ValidationError("запрещеный URL.")
