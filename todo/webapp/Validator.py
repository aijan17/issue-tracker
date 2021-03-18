from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


@deconstructible()
class TaskCreateForm(BaseValidator):
    message = "error on symbols, write letters"
    code = "too_symbol"

    def compare(self, a, b):
        return len(set(b) & set(a)) > 0



