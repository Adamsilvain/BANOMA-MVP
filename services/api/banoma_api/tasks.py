import subprocess
from celery import shared_task


@shared_task
def transcode_video(video_id: int, source_url: str):
    """Transcode une vidéo de portfolio en HLS via ffmpeg.
    TODO: uploader la sortie (.m3u8 + segments .ts) vers MinIO/S3 et mettre à jour
    `Video.file_url` avec l'URL finale une fois l'upload terminé."""
    output = f"/tmp/output-{video_id}.m3u8"
    cmd = [
        "ffmpeg", "-i", source_url,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-g", "48", "-sc_threshold", "0",
        "-f", "hls", "-hls_time", "4", "-hls_playlist_type", "vod",
        output,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return {"status": "done", "output": output}
    except subprocess.CalledProcessError as exc:
        return {"status": "failed", "error": exc.stderr.decode(errors="ignore")}
