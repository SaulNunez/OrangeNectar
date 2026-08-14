import csv
import io
from typing import List, Union

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models.saved_models import Comment, Submission

router = APIRouter()


@router.post("/export")
def export_posts(posts: List[Union[Comment, Submission]]):
    buffer = io.StringIO()
    fieldnames = sorted({field for post in posts for field in post.model_dump().keys()})
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for post in posts:
        writer.writerow(post.model_dump())
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=saved_posts.csv"},
    )
