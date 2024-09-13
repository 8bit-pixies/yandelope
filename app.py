import os
import sys
import tkinter as tk
from tkinter import ttk
from yt_dlp import YoutubeDL
from options import OPTIONS
from threading import Thread
from pathlib import Path
import io
from contextlib import redirect_stdout
import tkinter as tk # Python 3.x
import tkinter.scrolledtext as ScrolledText
import logging

try:
    from ctypes import windll  # Only exists on Windows.

    app_id = "com.application"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
except ImportError:
    pass

try:
    icon_png_path = "icon.png" if Path("icon.png").exists() else str(Path(sys._MEIPASS).joinpath("icon.png"))
except Exception as _:
    # not using pyinstaller
    icon_png_path = "icon.png"
    pass


class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)
        
class StreamToLogger:
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, level):
       self.logger = logger
       self.level = level
       self.linebuf = ''

    def write(self, buf):
       for line in buf.rstrip().splitlines():
          self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass


class AsyncDownload(Thread):
    def __init__(self, url, download_config):
        super().__init__()

        self.html = None
        self.url = url
        self.download_config = download_config

    def run(self):
        with YoutubeDL(OPTIONS.get(self.download_config, OPTION_480P)) as ydl:
            ydl.download([self.url])


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack(padx=10, pady=10, fill=tk.X, expand=True)
                
        self.url = tk.StringVar()
        self.selected_config = tk.StringVar()

        # URL input
        self.url_label = ttk.Label(self, text="URL Address:")
        self.url_label.pack(fill=tk.X, expand=True)

        self.url_entry = ttk.Entry(self, textvariable=self.url)
        self.url_entry.pack(fill=tk.X, expand=True)
        self.url_entry.focus()

        self.label = ttk.Label(self, text="Preset Configuration:")
        self.label.pack(fill=tk.X, expand=True)
        self.config_cb = ttk.Combobox(self, textvariable=self.selected_config)
        self.config_cb["values"] = list(OPTIONS.keys())

        # prevent typing a value
        self.config_cb["state"] = "readonly"
        self.config_cb.pack(fill=tk.X, expand=True)
        self.config_cb.set(list(OPTIONS.keys())[0])

        ttk.Label(self, text="").pack(fill=tk.X, expand=True) # add space for prettier setup

        self.pb = ttk.Progressbar(self, orient="horizontal", mode="indeterminate")
        self.pb.pack(fill=tk.X, expand=True)
        self.pb.pack_forget()

        self.status_label = ttk.Label(self, text="Download Complete")
        self.status_label.pack(fill=tk.X, expand=True)
        self.status_label.pack_forget()

        self.button = ttk.Button(self, text="Download 🦌", command=self.handle_button_press)
        self.button.pack(fill=tk.X, expand=True)

        # Add text widget to display logging info
        self.st = ScrolledText.ScrolledText(self, height=10)

        # Create textLogger
        self.text_handler = TextHandler(self.st)

        # Add the handler to logger
        self.logger = logging.getLogger()        
        self.logger.addHandler(self.text_handler)
        sys.stdout = StreamToLogger(self.logger, logging.ERROR)
        sys.stderr = StreamToLogger(self.logger, logging.ERROR)
        
        

    def monitor(self, thread):
        if thread.is_alive():
            # check the thread every 100ms
            self.pb.pack(fill=tk.X, expand=True)
            self.pb.start()
            self.st.pack(fill=tk.X, expand=True)
            self.status_label.pack_forget()
            self.button.pack_forget()
            self.after(100, lambda: self.monitor(thread))
        else:
            self.pb.stop()
            self.pb.pack_forget()
            self.button.pack(fill=tk.X, expand=True)
            self.status_label.pack(fill=tk.X, expand=True)        
            self.st.pack(fill=tk.X, expand=True)
            self.button["state"] = tk.NORMAL


    def handle_button_press(self):
        download_thread = AsyncDownload(
            url=self.url.get(), download_config=self.selected_config.get()
        )
        download_thread.start()
        self.monitor(download_thread)





root = tk.Tk()
root.geometry("400x360")
root.title("Yandelope")
# Set window icon.
app = Application(root)
app.master.iconphoto(False, tk.PhotoImage(file=icon_png_path))
app.mainloop()
