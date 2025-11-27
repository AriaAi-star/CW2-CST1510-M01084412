# %%

# Load the bcrypt library, which is used for password hashing.
import bcrypt

import os

# Create a function with a parameter ‘password’ of type string.



def hash_password (plain_password_text):

# Convert the password from a plain text string into a bytes field because bcrypt can only handle bytes-like objects.

    byted_password = plain_password_text.encode('utf-8')

# Generate a salt value randomly so as to add an extra level of security against a "rainbow table" attack.

    salt = bcrypt.gensalt()

# Hash the password with the salt value using the bcrypt hashing algorithm.

    final_hashed_password = bcrypt.hashpw (byted_password,salt)

# Convert the hashed password bytes into a UTF-8 string 

    return final_hashed_password.decode('utf-8')

# the bellow code is for test and there is no need to this 
#if __name__ == "__main__":
     #print(hash_password("Aria@1382"))

# %%


def password_verification (plain_password_text,final_hashed_password):

    byted_password = plain_password_text.encode('utf-8')

    final_hashed_password = final_hashed_password.encode('utf-8')

    return bcrypt.checkpw(byted_password,final_hashed_password)

# the bellow code is just for testing 

'''
test_password = "Aria@1382"
hashed = hash_password(test_password)
print(f"Original password: {test_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")
is_valid = password_verification(test_password, hashed)
print(f"\nVerification with correct password: {is_valid}")
is_invalid = password_verification("WrongPassword", hashed)
print(f"Verification with incorrect password: {is_invalid}")
'''




# %%
