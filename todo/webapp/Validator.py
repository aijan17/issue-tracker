from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


@deconstructible()
class TaskCreateForm(BaseValidator):
    message = "error on symbols, write letters"
    code = "too_symbol"

    def compare(self, a, b):
        return len(set(b) & set(a)) > 0


@deconstructible
class MinLengthValidator(BaseValidator):
    message = 'Value "%(value)s" has length of %(show_value)d! It should be at least %(limit_value)d symbols long!'
    code = 'too_short'

    def compare(self, a, b):
        return a < b

    def clean(self, x):
        return len(x)

