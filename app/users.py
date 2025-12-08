"""User management module.

Provides password hashing, validation, and user authentication utilities.
"""

import bcrypt

#PASSWORD HASHING AND VERIFICATION
# WE NEED TO HASH A PASSWORD AND ALSO ADD A SOLT TO IT TO MAKE IT ENOUGH SECURE
def hash_password(plain_password_text):
    """Hash a plain text password using bcrypt."""
    byted_password=plain_password_text.encode('utf-8')
    salt=bcrypt.gensalt()
    final_hashed_password=bcrypt.hashpw(byted_password, salt)
    return final_hashed_password.decode('utf-8')


def password_verification(plain_password_text, final_hashed_password):
    """Verify a plain text password against a bcrypt hash."""
    byted_password = plain_password_text.encode('utf-8')
    final_hashed_password = final_hashed_password.encode('utf-8')
    return bcrypt.checkpw(byted_password, final_hashed_password)


#PASSWORD STRENGTH CHECKER


def check_password(password):
    """Display password strength feedback."""
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_space = any(ch.isspace() for ch in password)
    has_special = any(ch in "!@#$%^&*()_+-=[]{}|;:',.<>?/\\~`" for ch in password)

    if has_upper:
        print("✓ Your password has an uppercase letter.")
    else:
        print("✗ Your password does NOT have an uppercase letter.")

    if has_lower:
        print("✓ Your password has a lowercase letter.")
    else:
        print("✗ Your password does NOT have a lowercase letter.")

    if has_digit:
        print("✓ Your password has a digit.")
    else:
        print("✗ Your password does NOT have any digits.")

    if has_special:
        print("✓ Your password has a special character.")
    else:
        print("✗ Your password does NOT have a special character.")

    if has_space:
        print("⚠ Your password contains spaces. Please remove them.")
    else:
        print("✓ Your password does not contain spaces.")
