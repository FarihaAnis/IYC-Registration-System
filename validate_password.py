def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    special_characters = set("!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~")

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    conditions_met = sum([has_upper, has_lower, has_digit, has_special])

    if conditions_met >= 3:
        return True, "Password is valid."
    else:
        return False, "Password must contain at least three of the following: uppercase letter, lowercase letter, number, special character."