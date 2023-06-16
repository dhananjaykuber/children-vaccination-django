import re


def phone_number_validator(phone_number):
    if not phone_number.isdigit():
        raise Exception("Phone number must be valid digits.")
    if not len(phone_number) == 10:
        raise Exception("Phone number must be of 10 digits.")


def email_validator(email):
    pattern = r"^[\w\._]+@[\w\.]+\.\w+$"

    if not re.match(pattern, email):
        raise Exception("Email must be valid.")
