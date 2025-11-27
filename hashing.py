
# instructor

'''
import bcrypt

def hash_password(plain_text_password):
    # Encode the password to bytes, required by bcrypt
    password_bytes = plain_text_password.encode('utf-8')

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    # Return the hashed password as a decoded string
    return hashed_password.decode('utf-8')

## test|_hasshing
## if __name__ == "__main__":
    print(hash_password("Aria@1382"))


def verify_password(plain_text_password, hashed_password):
    # Convert both plaintext and stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')

    # bcrypt.checkpw extracts salt from the hash and compares
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


def register_user(username, password):
    """Register a new user."""
    
    hashed_password = hash_password(password)
    
    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")
    
    print(f"User '{username}' registered.")


def login_user(username, password):
    """Log in an existing user."""
    
    with open("users.txt", "r") as f:
        for line in f.readlines():
            user, hash = line.strip().split(',', 1)
            
            if user == username:
                return verify_password(password, hash)
    
    return False
'''