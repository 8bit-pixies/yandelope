from time import sleep
import dearpygui.dearpygui as dpg
from threading import Thread
import dearpygui_ext.logger as dpg_logger
from yt_dlp import YoutubeDL


class AsyncTask(Thread):
    def __init__(self, url, download_config):
        super().__init__()

        self.html = None
        self.url = url
        self.download_config = download_config

    def run(self):
        params = OPTIONS.get(self.download_config, OPTION_480P)
        params["logger"] = logger
        logger.error = logger.log_error
        logger.debug = logger.log_debug
        with YoutubeDL(params) as ydl:
            ydl.download([self.url])


class LoadingHandler:
    def __init__(self):
        _in_progress = ["-", "\\", "|", "/"]
        self.loading_text = [f"Loading... {x}" for x in _in_progress]

    @property
    def initial_state(self):
        return self.loading_text[0]

    def next(self, state=None):
        index = self.loading_text.index(state) - 1 if state in self.loading_text else 0
        return self.loading_text[index]


OPTION_480P = {
    "extract_flat": "discard_in_playlist",
    "format": "(mp4)[height<=480]+ba/(mp4)[height<=480] / wv*+ba/w",
    "fragment_retries": 10,
    "ignoreerrors": "only_download",
    "postprocessors": [
        {"key": "FFmpegConcat", "only_multi_video": True, "when": "playlist"}
    ],
    "retries": 10,
}

OPTION_AUDIO_ONLY = {
    "extract_flat": "discard_in_playlist",
    "format": "(mp4)wa",
    "fragment_retries": 10,
    "ignoreerrors": "only_download",
    "postprocessors": [
        {"key": "FFmpegConcat", "only_multi_video": True, "when": "playlist"}
    ],
    "retries": 10,
}

OPTION_144P = {
    "extract_flat": "discard_in_playlist",
    "format": "(mp4)[height<=144]+ba/(mp4)[height<=144] / wv*+wa/w",
    "fragment_retries": 10,
    "ignoreerrors": "only_download",
    "postprocessors": [
        {"key": "FFmpegConcat", "only_multi_video": True, "when": "playlist"}
    ],
    "retries": 10,
}

OPTIONS = {"144p": OPTION_144P, "480p": OPTION_480P, "audio-only": OPTION_AUDIO_ONLY}
OPTION_DEFAULT = "480p"

LOADING_INFO_DEFAULT = "Waiting..."

dpg.create_context()


def run_job():
    # dpg.get_value("url")
    dpg.set_value("loading_info", LoadingHandler().initial_state)
    dpg.configure_item("button_job", enabled=False, label="Job is Running...")
    job = AsyncTask(dpg.get_value("url"), dpg.get_value("download_config"))
    job.start()
    while hasattr(job, "is_alive") and job.is_alive():
        dpg.set_value(
            "loading_info", LoadingHandler().next(dpg.get_value("loading_info"))
        )
        sleep(0.125)
    dpg.configure_item("button_job", enabled=True, label="Run Job")
    dpg.set_value("loading_info", LOADING_INFO_DEFAULT)


with dpg.window(tag="Window") as primary_window:
    dpg.add_input_text(
        label="URL", tag="url", source="string_value", default_value="<enter url here>"
    )
    dpg.add_combo(
        tag="download_config", items=list(OPTIONS.keys()), default_value=OPTION_DEFAULT
    )
    dpg.add_button(label="Run Job", tag="button_job", callback=run_job)
    dpg.add_text(label="string", tag="loading_info", default_value=LOADING_INFO_DEFAULT)
    with dpg.child_window(tag="LogWindow", height=-1):
        logger = dpg_logger.mvLogger("LogWindow")


dpg.set_primary_window(primary_window, True)
dpg.create_viewport(title="Window", width=600, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
