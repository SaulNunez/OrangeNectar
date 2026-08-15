import csv
import io
from typing import List, Literal, Optional, Tuple, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from openpyxl import Workbook

from models.saved_models import Comment, Submission
from routers.reddit import get_reddit_service
from services.html_export import build_export_zip
from services.reddit_service import RedditService

router = APIRouter()

SavedItem = Union[Comment, Submission]

COMMENT_FIELDS = list(Comment.model_fields.keys())
SUBMISSION_FIELDS = list(Submission.model_fields.keys())

XLSX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
ZIP_MEDIA_TYPE = "application/zip"


def _split_posts(posts: List[SavedItem]) -> Tuple[List[Submission], List[Comment]]:
    submissions = [post for post in posts if isinstance(post, Submission)]
    comments = [post for post in posts if isinstance(post, Comment)]
    return submissions, comments


def _posts_to_csv(posts: List[SavedItem], fieldnames: List[str]) -> io.StringIO:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for post in posts:
        writer.writerow(post.model_dump())
    buffer.seek(0)
    return buffer


def _write_sheet(sheet, fieldnames: List[str], items: List[SavedItem]) -> None:
    sheet.append(fieldnames)
    for item in items:
        data = item.model_dump()
        sheet.append([data[field] for field in fieldnames])


def _posts_to_xlsx(posts: List[SavedItem]) -> io.BytesIO:
    submissions, comments = _split_posts(posts)

    workbook = Workbook()
    posts_sheet = workbook.active
    posts_sheet.title = "Posts"
    _write_sheet(posts_sheet, SUBMISSION_FIELDS, submissions)

    comments_sheet = workbook.create_sheet("Comments")
    _write_sheet(comments_sheet, COMMENT_FIELDS, comments)

    buffer = io.BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return buffer


@router.get("/export")
def export_posts(
    kind: Literal["all", "posts", "comments"] = "all",
    subreddit: Optional[str] = Query(
        default=None, description="Only include subreddits containing this substring (case-insensitive)"
    ),
    format: Literal["csv", "xlsx", "html"] = "csv",
    reddit_service: RedditService = Depends(get_reddit_service),
):
    posts = reddit_service.fetch_saved_posts()

    if kind == "posts":
        posts = [post for post in posts if isinstance(post, Submission)]
        fieldnames = SUBMISSION_FIELDS
    elif kind == "comments":
        posts = [post for post in posts if isinstance(post, Comment)]
        fieldnames = COMMENT_FIELDS
    else:
        fieldnames = sorted(set(COMMENT_FIELDS) | set(SUBMISSION_FIELDS))

    if subreddit:
        posts = [post for post in posts if subreddit.lower() in post.subreddit.lower()]

    if not posts:
        raise HTTPException(status_code=404, detail="No saved posts found matching the given filters")

    if format == "xlsx":
        return StreamingResponse(
            _posts_to_xlsx(posts),
            media_type=XLSX_MEDIA_TYPE,
            headers={"Content-Disposition": "attachment; filename=saved_posts.xlsx"},
        )

    if format == "html":
        submissions, comments = _split_posts(posts)
        return StreamingResponse(
            build_export_zip(submissions, comments),
            media_type=ZIP_MEDIA_TYPE,
            headers={"Content-Disposition": "attachment; filename=saved_posts.zip"},
        )

    return StreamingResponse(
        _posts_to_csv(posts, fieldnames),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=saved_posts.csv"},
    )
