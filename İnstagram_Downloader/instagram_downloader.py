import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import instaloader

def download_instagram_post(url, status_callback):
    if not instaloader:
        status_callback('Instaloader yüklü değil!')
        messagebox.showerror('Hata', 'Instaloader kütüphanesi yüklü değil!')
        return
    loader = instaloader.Instaloader()
    try:
        shortcode = url.strip().split('/')
        shortcode = [s for s in shortcode if s]
        if 'p' in shortcode:
            idx = shortcode.index('p')
            code = shortcode[idx+1]
        else:
            code = shortcode[-1]
        loader.download_post(instaloader.Post.from_shortcode(loader.context, code), target="downloads")
        status_callback('Instagram postu indirildi!')
    except Exception as e:
        status_callback(f'Hata: {e}')
        messagebox.showerror('Hata', f'İndirme hatası:\n{e}')

class InstagramDownloaderApp:
    def __init__(self, root):
        self.root = root
        root.title("Instagram Post İndirici")
        root.geometry("400x200")
        self.url = tk.StringVar()
        self.status = tk.StringVar()

        ttk.Label(root, text="Instagram Post Linki:").pack(pady=10)
        ttk.Entry(root, textvariable=self.url, width=50).pack(pady=5)
        ttk.Button(root, text="İndir", command=self.start_download).pack(pady=10)
        ttk.Label(root, textvariable=self.status, foreground="blue").pack(pady=5)

    def set_status(self, msg):
        self.status.set(msg)

    def start_download(self):
        url = self.url.get().strip()
        if not url:
            self.set_status("Lütfen bir link girin!")
            return
        self.set_status("İndiriliyor...")
        threading.Thread(target=self.download, args=(url,), daemon=True).start()

    def download(self, url):
        download_instagram_post(url, self.set_status)

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    root = tk.Tk()
    app = InstagramDownloaderApp(root)
    root.mainloop() 