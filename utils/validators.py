from django.core.validators import RegexValidator


LETTER_SPACE_DASH_VALIDATOR = RegexValidator(r'^[a-zA-ZÀ-ÿ\s-]*$', 'Seules les lettres, espaces et tirets sont autorisés.')
