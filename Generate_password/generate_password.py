import tkinter as tk
from tkinter import ttk, messagebox
import string
import random
from cryptography.fernet import Fernet

#Creates a key for encryption. Please do not delete or lose the generated file.
try:
    with open("key.key", "rb") as kf:
        key = kf.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open("key.key", "wb") as kf:
        kf.write(key)
fernet = Fernet(key)

def generate_password(length, num_digits, num_symbols):
    digits = string.digits
    symbols = "!@#$%^&*()-_=+"
    all_letters = string.ascii_letters # .ascii_lowercase + .ascii_uppercase

    if num_digits + num_symbols > length:
        messagebox.showerror("Error", "The total number of digits and symbols cannot exceed the password length.")
        return None # Stop if error

    password_char = []
    for i in range(num_digits):
        password_char.append(random.choice(digits))
    for y in range(num_symbols):
        password_char.append(random.choice(symbols))
    
    remaining = length - len(password_char)
    for z in range(remaining):
        password_char.append(random.choice(all_letters))
    
    random.shuffle(password_char)
    return "".join(password_char)

#Encrypt - Decrypt password
def encrypt_pwd(pwd):
    return fernet.encrypt(pwd.encode())

def decrypt_line(enc_line):
    return fernet.decrypt(enc_line.strip()).decode()


#Main function called when the button is clicked.
def handle_generate_button_click():
    try:
        # Get data from the interface
        length = int(len_entry.get())
        num_digits = int(digit_entry.get())
        num_symbols = int(symbol_entry.get())
        explanation = desc_entry.get()

        if not explanation:
            messagebox.showwarning("Missing Information", "Please fill in the 'Description' field.")
            return
        
        # Generate password
        password = generate_password(length, num_digits, num_symbols)

        if password is None:
            return

        # Write result
        encrypted = encrypt_pwd(f"My password for {explanation}: {password}")
        with open("password.txt", mode="a", encoding="utf-8") as password_file:
            password_file.write(encrypted.decode() + "\n")
        
        messagebox.showinfo("Success", f"Password for '{explanation}' is {password}")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers in all numeric fields.")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An error occurred: {e}")

def show_passwords():
    try:
        with open("password.txt", "r", encoding="utf-8") as pf:
            lines = [decrypt_line(line.encode()) for line in pf if line.strip()]
    except FileNotFoundError:
        lines = ["No saved passwords yet."]
    except Exception as e:
        lines = [f"Error reading file: {e}"]
    messagebox.showinfo("Saved Passwords", "\n".join(lines))


#Main window
window = tk.Tk()
window.title("Password Generator")
window.geometry("450x300")

# Style
style = ttk.Style(window)
style.theme_use("clam")

# Place widgets
generator_frame = ttk.LabelFrame(window, text="Generate New Password", padding=(20, 10))
generator_frame.pack(padx=10, pady=10, fill="x", expand=True)

#Description entry
ttk.Label(generator_frame, text="Description (e.g. Gmail):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
desc_entry = ttk.Entry(generator_frame, width=30)
desc_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

#Length entry
ttk.Label(generator_frame, text="Password Length:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
len_entry = ttk.Entry(generator_frame, width=10)
len_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
len_entry.insert(0, "16")

#Digit entry
ttk.Label(generator_frame, text="Number of Digits:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
digit_entry = ttk.Entry(generator_frame, width=10)
digit_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
digit_entry.insert(0, "4")

#Symbol entry
ttk.Label(generator_frame, text="Number of Symbols:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
symbol_entry = ttk.Entry(generator_frame, width=10)
symbol_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
symbol_entry.insert(0, "2")

# Call function
generate_button = ttk.Button(generator_frame, text="Generate and Save", command=handle_generate_button_click)
generate_button.grid(row=4, column=0, columnspan=2, pady=20)

# Show button
show_button = ttk.Button(generator_frame, text="Show Saved Passwords", command=show_passwords)
show_button.grid(row=5, column=0, columnspan=2, pady=5)

window.mainloop()