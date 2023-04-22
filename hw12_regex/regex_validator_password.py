import re


def validator_password(password):
    if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
        print("Password is valid")
        return True
    if len(password) < 8:
        print("Password is too short, it must be at least 8 characters long")
    if not re.search(r'[a-z]', password):
        print("Password must contain at least one lowercase letter")
    if not re.search(r'[A-Z]', password):
        print("Password must contain at least one uppercase letter")
    if not re.search(r'\d', password):
        print("Password must contain at least one digit")
    if not re.search(r'[@$!%*?&]', password):
        print("Password must contain at least one special character")
    return False


validator_password(input('Input your password: '))
