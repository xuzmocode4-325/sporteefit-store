from ninja import Schema
from typing import List, Optional, Any, Dict, Union
from datetime import date
from pydantic import Field, ConfigDict

class AuthorSchema(Schema):
    id: int
    name: str
    bio: str
    image: Optional[str] = None  # If Author has image; confirm model

class GalleryImageSchema(Schema):
    image: str  # URL via resolver
    caption: Optional[str] = None

class StreamBlockSchema(Schema):
    type: str
    value: Dict[str, Any] = {}

class BlogPostListSchema(Schema):
    id: int
    title: str
    slug: str
    date: date
    quote: Optional[str] = None
    intro: Optional[str] = None
    first_image: Optional[GalleryImageSchema] = None
    authors: List[AuthorSchema] = []
    category: Optional[str] = None
    tags: List[str] = []

    model_config = ConfigDict(
        json_schema_extra={
            'fields': ['id', 'title', 'slug', 'date', 'quote', 'intro', 'first_image', 'authors', 'category', 'tags']
        }
    )


class BlogPostDetailSchema(Schema):
    id: int
    title: str
    slug: str
    date: date
    quote: Optional[str] = None
    intro: Optional[str] = None
    body: List[Dict[str, Any]] = []  # Raw Wagtail JSON ONLY
    authors: List[Dict[str, Any]] = []
    tags: List[str] = []
    gallery_images: List[Dict[str, Any]] = []
    category: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            'fields': [
                'id', 'title', 'slug', 'date', 'intro', 
                'body', 'authors', 'tags', 'gallery_images', 'category'
            ]
        }
    )
