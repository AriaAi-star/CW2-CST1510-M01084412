def hash_password(plain_password_text):
    byted_password = plain_password_text.encode('utf-8')
    salt = bcrypt.gensalt()
    final_hashed_password = bcrypt.hashpw(byted_password, salt)
    return final_hashed_password.decode('utf-8')


def password_verification(plain_password_text, final_hashed_password):
    byted_password = plain_password_text.encode('utf-8')
    final_hashed_password = final_hashed_password.encode('utf-8')
    return bcrypt.checkpw(byted_password, final_hashed_password)


# -----------------------------
# User Registration
# -----------------------------
def register_user(username, password):
    hashed_password = hash_password(password)
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_password}\n")
    print(f"User '{username}' registered.")

# -----------------------------
# Check if Username Exists
# -----------------------------
def user_exists(username):
    try:
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                stored_username, _ = line.strip().split(",", 1)
                if stored_username == username:
                    return True
    except FileNotFoundError:
        return False
    return False


# -----------------------------
# Login (bcrypt verification)
# -----------------------------
def login_user(username, password):
    try:
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                stored_username, stored_hash = line.strip().split(",", 1)
                if stored_username == username:
                    return password_verification(password, stored_hash)
    except FileNotFoundError:
        return False
    return False


# -----------------------------
# Password Requirements Display
# -----------------------------
def check_password(password):
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_space = any(ch.isspace() for ch in password)
    has_special = any(ch in string.punctuation for ch in password)

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


# -----------------------------
# Username & Password Validation
# -----------------------------
def validate_username(username):
    import re
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if not username[0].isalpha():
        return False, "Username must start with a letter."
    if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", username):
        return False, "Username can only contain letters, digits, and underscores."
    if user_exists(username):
        return False, "This username is already taken."
    return True, ""


def validate_password(password):
    import re
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain a lowercase letter."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain an uppercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain a digit."
    if not re.search(r'[\W_]', password):
        return False, "Password must contain a special character."
    if " " in password:
        return False, "Password must not contain spaces."
    return True, ""