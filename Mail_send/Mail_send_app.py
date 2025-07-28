import smtplib, ssl
import tkinter as tk
from tkinter import messagebox,ttk,scrolledtext,filedialog
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from PIL import Image, ImageTk

attached_file_path = "" 
#Sending email
def send_email_logic(sender,password,receiver,message):
    context = ssl.create_default_context()
    smtp_server = "smtp.gmail.com"
    port = 465

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender, password)
            server.send_message(message)
        messagebox.showinfo(title="Success", message="Email sent successfully.")
        
    except:
        messagebox.showerror(title="Error", message="Failed to send email.")


def upload_file():
   global attached_file_path
   file_path = filedialog.askopenfilename()
   if file_path:
       attached_file_path = file_path   
       file_label.config(text=os.path.basename(file_path)) 

#Retrieving information from the interface
def handle_send_button_click():
    sender = sender_email_entry.get()
    password = password_entry.get()
    receiver = receiver_emails_entry.get()
    subject = subject_entry.get()
    message = message_text.get("1.0", tk.END)

    if not all([sender, password, receiver, subject, message.strip()]):
        messagebox.showerror(title="Error", message="Please fill in all fields.")
        return

    receiver_list = [email.strip() for email in receiver.split(",") if email.strip()]

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = ", ".join(receiver_list)
    message["Subject"] = subject
    message.attach(MIMEText(message_text.get("1.0", tk.END), "plain"))

    if attached_file_path:
        try:
            with open(attached_file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {attached_file_path.split('/')[-1]}",
                )
                message.attach(part)
        except Exception as e:
            print(f"Error attaching file: {e}")

    send_email_logic(sender, password, receiver_list, message)


#GUI
window = tk.Tk()
window.title("Email Sender")
window.geometry("650x1000")

#Style
style = ttk.Style(window)
style.theme_use("clam")

#Place widgets
sender_frame = ttk.LabelFrame(window, text="Sender Information", padding=(20, 10))
sender_frame.pack(padx=10, pady=10, fill="x")

#Sender area
ttk.Label(sender_frame, text="Sender Email:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
sender_email_entry = ttk.Entry(sender_frame, width=40)
sender_email_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
sender_email_entry.insert(0, "")

#Password area
ttk.Label(sender_frame, text="Application Password:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
password_entry = ttk.Entry(sender_frame, width=40, show="*")
password_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

#Recipient frame
receiver_frame = ttk.LabelFrame(window, text="Recipient Information", padding=(20, 10))
receiver_frame.pack(padx=10, pady=10, fill="x")

#Recipient area
ttk.Label(receiver_frame, text="Recipient Email - Emails").grid(row=0, column=0, sticky="w", padx=5, pady=5)
receiver_emails_entry = ttk.Entry(receiver_frame, width=40)
receiver_emails_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
ttk.Label(receiver_frame, text="If there is more than one, separate them with commas.").grid(row=1, column=1, sticky="w", padx=5)

#Message frame
message_frame = ttk.LabelFrame(window, text="Mail content", padding=(20, 10))
message_frame.pack(padx=10, pady=10, fill="both", expand=True)

#Subject area
ttk.Label(message_frame, text="Subject:").pack(anchor="w", padx=5)
subject_entry = ttk.Entry(message_frame)
subject_entry.pack(fill="x", padx=5, pady=(0, 10))

#Message area
ttk.Label(message_frame, text="Message:").pack(anchor="w", padx=5)
message_text = scrolledtext.ScrolledText(message_frame, height=10, font=("Helvetica", 10))
message_text.pack(fill="both", expand=True, padx=5, pady=5)

#File frame
file_frame = ttk.LabelFrame(window, text="File", padding=(20, 10))
file_frame.pack(padx=10, pady=10, fill="x")

#File button
file_button = ttk.Button(file_frame, text="Attach File", command=upload_file)
file_button.pack(side="left", padx=(0, 10))
file_label = ttk.Label(file_frame, text="No file selected")
file_label.pack(side="left")

 #Send Button
send_button = ttk.Button(window,text="Send Email", command=handle_send_button_click)
send_button.pack(pady=20)




if __name__ == "__main__":
    window.mainloop()
