manifest = {
    "name": "Converter Plugin",
    "version": "1.0.0",
    "description": "Media conversion engine",
    "enabled": True,
}

config = {
    "ffmpeg_path": "ffmpeg",
    "supported_conversions": [
        "text_to_voice", "voice_to_text", "video_to_round",
        "round_to_video", "audio_to_voice", "video_to_audio",
    ],
}
