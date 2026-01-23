import re
from django.core.exceptions import ValidationError

class CustomPasswordComplexityValidator:
    def validate(self, password, user=None):
        if ' ' in password:
            raise ValidationError(
                "Password must not contain spaces.",
                code='password_no_space',
            )


        special_char_regex = re.compile(r'[^a-zA-Z0-9\s]')
        if not special_char_regex.search(password):
            raise ValidationError(
                "Password must contain at least one special character.",
                code='password_no_special_char',
            )

    def get_help_text(self):
        return (
            "Your password must be at least 8 characters, contain no spaces, "
            "and include at least one special character."
        )