from fastapi import APIRouter, HTTPException
from models.post_models import Post

router = APIRouter()

@router.post("/export")
def export_posts(posts: list[Post]):
    pass

