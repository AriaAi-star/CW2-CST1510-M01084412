"""User management module.

Provides password hashing, validation, and user authentication utilities.
"""

import bcrypt
import re
import sqlite3
from pathlib import Path


def hash_password(plain_password_text):
    """Hash a plain text password using bcrypt."""
    byted_password = plain_password_text.encode('utf-8')
    salt = bcrypt.gensalt()
    final_hashed_password = bcrypt.hashpw(byted_password, salt)
    return final_hashed_password.decode('utf-8')


def password_verification(plain_password_text, final_hashed_password):
    """Verify a plain text password against a bcrypt hash."""
    byted_password = plain_password_text.encode('utf-8')
    final_hashed_password = final_hashed_password.encode('utf-8')
    return bcrypt.checkpw(byted_password, final_hashed_password)


def validate_username(username):
    """Validate username format."""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if not username[0].isalpha():
        return False, "Username must start with a letter."
    if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", username):
        return False, "Username can only contain letters, digits, and underscores."
    return True, ""


def validate_password(password):
    """Validate password strength requirements."""
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


def migrate_users_from_file(conn, filepath=None):
    """Migrate users from users.txt file to database.
    
    Args:
        conn: Database connection
        filepath: Path to users.txt file (defaults to DATA/users.txt)
    """
    if filepath is None:
        filepath = Path("DATA/users.txt")
    else:
        filepath = Path(filepath)
    
    if not filepath.exists():
        print(f"⚠️  File not found: {filepath}")
        print("   No users to migrate.")
        return
    
    cursor = conn.cursor()
    migrated_count = 0
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse line: username,password_hash
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                
                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")
    
    conn.commit()
    print(f"✅ Migrated {migrated_count} users from {filepath.name}")
