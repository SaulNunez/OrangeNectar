import io
import zipfile
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

import httpx
from jinja2 import Environment, FileSystemLoader, select_autoescape

from models.saved_models import Comment, Submission

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VIDEO_EXTENSION = ".mp4"

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html"]),
)


def _image_extension(url: str) -> Optional[str]:
    path = urlparse(url).path.lower()
    for extension in IMAGE_EXTENSIONS:
        if path.endswith(extension):
            return extension
    return None


def _download_file(url: str) -> Optional[bytes]:
    try:
        response = httpx.get(url, timeout=10.0, follow_redirects=True)
        response.raise_for_status()
        return response.content
    except httpx.HTTPError:
        return None


def build_export_zip(submissions: List[Submission], comments: List[Comment]) -> io.BytesIO:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        submission_images: Dict[str, str] = {}
        submission_videos: Dict[str, str] = {}

        for submission in submissions:
            extension = _image_extension(submission.url)
            if extension is not None:
                image_bytes = _download_file(submission.url)
                if image_bytes is not None:
                    filename = f"{submission.id}{extension}"
                    archive.writestr(f"img/{filename}", image_bytes)
                    submission_images[submission.id] = f"img/{filename}"

            if submission.video_url:
                video_bytes = _download_file(submission.video_url)
                if video_bytes is not None:
                    filename = f"{submission.id}{VIDEO_EXTENSION}"
                    archive.writestr(f"videos/{filename}", video_bytes)
                    submission_videos[submission.id] = f"videos/{filename}"

        template = _env.get_template("export.html")
        html = template.render(
            submissions=submissions,
            comments=comments,
            submission_images=submission_images,
            submission_videos=submission_videos,
        )
        archive.writestr("index.html", html)

    zip_buffer.seek(0)
    return zip_buffer
