# Week 7: Secure Authentication System  
Student Name:ARIA KARIMPOUR  
Student ID:M01084412
Course: CST1510 - CW2 -  

---

## Project Description  
This project is a command-line authentication system written in Python.  
It allows users to register and log in using a secure password hashing mechanism based on bcrypt.  
User data is stored in a simple text file.

---

## Features  
- User registration with unique username check  
- Secure password hashing using bcrypt (with automatic salt generation)  
- User login with password verification  
- Input validation for usernames and passwords  
- File-based user data persistence in `users.txt`  

---

## Technical Details  

- **Language:** Python  
- **Hashing:** bcrypt (`hashpw`, `gensalt`, `checkpw`)  
- **Storage:** `users.txt` with lines in the format:  
  `username,hashed_password`  

- **Username validation:**  
  - At least 3 characters  
  - Starts with a letter  
  - Only letters, digits and underscores  
  - Must not already exist in the file  

- **Password validation:**  
  - At least 8 characters  
  - Contains uppercase, lowercase, digit and special character  
  - No spaces  

---

## How to Run  

1. Install dependencies (bcrypt):  
   ```bash
   pip install bcrypt
