import re

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def validate_registration(name, mail, psw, psw2, errors_list):
        """
        Validate user registration input.

        Checks for empty fields, name length, email format,
        password length, password complexity, and matching passwords.

        Args:
            name (str): User's name.
            mail (str): User's email.
            psw (str): Password.
            psw2 (str): Password confirmation.
            errors_list (list): List of error messages to use.

        Returns:
            dict: Contains 'success' (bool) and 'errors' (list of messages).
        """
        errors = []

        if not all([name.strip(), mail.strip(), psw.strip(), psw2.strip()]):
            errors.append(errors_list[0])

        if len(name) < 2:
            errors.append(errors_list[1])

        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, mail):
            errors.append(errors_list[2])

        if len(psw) < 6:
            errors.append(errors_list[3])

        if not re.search(r'[A-Za-z]', psw) or not re.search(r'\d', psw):
            errors.append(errors_list[4])

        if psw != psw2:
            errors.append(errors_list[5])

        return {"success": not errors, "errors": errors}


