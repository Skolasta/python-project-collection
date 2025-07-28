import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

# --- Constants and Key Derivation ---
SALT = b'your_very_secure_and_random_salt_for_your_encryption_project'
NOTES_FILE = "SecretNotes.bin"

def generate_key_from_password(password, salt):
    """Derives a secure Fernet key from the user's master password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Fernet key must be 32 bytes
        salt=salt,
        iterations=480000,  # Number of iterations for security
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

# --- Core Functions ---

def save_and_encrypt_note():
    """Saves and encrypts the current note to the file."""
    title = title_entry.get().strip()
    secret = secret_text.get("1.0", tk.END).strip()
    master_key = master_key_entry.get().strip()

    if not title or not secret or not master_key:
        messagebox.showwarning("Warning", "Please fill in all fields!")
        return

    try:
        fernet_key = generate_key_from_password(master_key, SALT)
        f = Fernet(fernet_key)

        encrypted_secret = f.encrypt(secret.encode())

        with open(NOTES_FILE, mode="ab") as notes_file:
            notes_file.write(title.encode() + b"\n")
            notes_file.write(encrypted_secret + b"\n")
            notes_file.write(b"---END_OF_NOTE---\n")
        
        messagebox.showinfo("Success", "Note saved and encrypted successfully!")
        
        # Clear the input fields
        title_entry.delete(0, tk.END)
        secret_text.delete("1.0", tk.END)
        master_key_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {e}")

def decrypt_notes():
    """Decrypts all notes from the file using the master key."""
    master_key = master_key_entry.get().strip()

    if not master_key:
        messagebox.showwarning("Warning", "Please enter your master key!")
        return

    try:
        if not os.path.exists(NOTES_FILE):
             messagebox.showinfo("Info", f"No notes file found ('{NOTES_FILE}').")
             return

        fernet_key = generate_key_from_password(master_key, SALT)
        f = Fernet(fernet_key)

        decrypted_content = ""
        
        with open(NOTES_FILE, mode="rb") as notes_file:
            lines = notes_file.readlines()
            
        i = 0
        notes_found = 0
        while i < len(lines):
            if i + 2 < len(lines):
                try:
                    title = lines[i].strip().decode()
                    encrypted_secret_line = lines[i+1].strip()
                    
                    decrypted_secret = f.decrypt(encrypted_secret_line).decode()
                    
                    decrypted_content += f"Title: {title}\nNote: {decrypted_secret}\n{'-'*20}\n"
                    notes_found += 1
                    i += 3 
                except Exception:
                    i += 3 
            else:
                i += 1 

        if notes_found > 0:
            secret_text.delete("1.0", tk.END)
            secret_text.insert(tk.END, decrypted_content)
            messagebox.showinfo("Success", f"{notes_found} note(s) decrypted successfully!")
        else:
            messagebox.showinfo("Info", "No valid notes could be decrypted. Please check your master key.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during decryption: {e}")

# --- Tkinter UI Setup ---
window = tk.Tk()
window.title("Secret Notes Application")
window.config(padx=30, pady=20)
window.minsize(450, 550)

# Title Entry
title_label = tk.Label(text="Title", font=("Arial", 12))
title_label.pack()
title_entry = tk.Entry(width=50)
title_entry.pack(pady=(0, 10))

# Secret Text Area
secret_label = tk.Label(text="Your Secret Note", font=("Arial", 12))
secret_label.pack()
secret_text = tk.Text(width=50, height=15)
secret_text.pack(pady=(0, 10))

# Master Key Entry
master_key_label = tk.Label(text="Master Key", font=("Arial", 12, "bold"))
master_key_label.pack()
master_key_entry = tk.Entry(width=50, show="*")
master_key_entry.pack(pady=(0, 20))

# Save & Encrypt Button
save_encrypt_button = tk.Button(text="Save & Encrypt Note", command=save_and_encrypt_note, font=("Arial", 10, "bold"))
save_encrypt_button.pack(pady=(0, 10))

# Decrypt Button
decrypt_button = tk.Button(text="Decrypt All Notes", command=decrypt_notes, font=("Arial", 10, "bold"))
decrypt_button.pack()

window.mainloop()
