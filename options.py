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