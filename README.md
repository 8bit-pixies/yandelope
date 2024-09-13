# Yandelope

Yandelope is a standalone GUI version of yt-dlp which is built using `pyinstaller` and `tkinter`. This project is more an experiment for learning `uv` and `pyinstaller` more than building a complete application.

# Development

Initialise your environment via `uv`. Then to start the application, you can use:

```sh
uv run pyinstaller -w --onefile --name "Yandelope" --icon=icon.ico app.py
```

To build the appropriate binary

