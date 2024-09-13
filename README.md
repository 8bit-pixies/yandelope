# Yandelope

Yandelope is a standalone GUI version of yt-dlp which is built using `pyinstaller` and `tkinter`. This project is more an experiment for learning `uv` and `pyinstaller` more than building a complete application.

# Development

Initialise your environment via `uv`. Then to start the application, you can use:

```sh
uv run pyinstaller -w --onefile --name "Yandelope" --icon=icon.ico --add-data="icon.ico:." --add-data="icon.png:." app.py
uv run pyinstaller -w --onefile --name "Yandelope2" --icon=icon.ico app2.py
```

To build the appropriate binary

