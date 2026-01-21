# api.py (or in your router file)
from ninja import Router
from django.shortcuts import get_object_or_404
from django.http import Http404
from typing import List
from wagtail.models import Page
from django.utils.html import strip_tags
from .models import BlogPostPage
from .schemas import BlogPostListSchema, BlogPostDetailSchema
from wagtail.rich_text import expand_db_html

router = Router(tags=['blog'])

def _abs_url(request, url: str):
    if not url:
        return ''
    try:
        return request.build_absolute_uri(url)
    except Exception:
        return url


def _add_first_image(request, post, schema_dict):
    """Helper to add first image (absolute url) to post data"""
    first_image = post.main_image()
    if first_image:
        caption = post.gallery_images.first().caption if post.gallery_images.first() else None
        schema_dict['first_image'] = {
            'image': _abs_url(request, first_image.file.url),
            'caption': caption
        }
    return schema_dict

def _strip_html(text):
    """Safely strip HTML from Wagtail RichText"""
    if not text:
        return ''
    return strip_tags(str(expand_db_html(text))).strip()

def _process_body_json(body_json):
    """Strip HTML from paragraph blocks, keep headings clean"""
    if not body_json:
        return []
    
    processed = []
    for block in body_json:
        if block['type'] == 'paragraph':
            # Strip HTML from RichTextBlock value
            block['value'] = _strip_html(block['value'])
        elif block['type'] == 'heading':
            # Headings already clean (text only)
            pass
        processed.append(block)
    return processed

@router.get('/posts/', response=List[BlogPostListSchema])
def blog_list(request):
    """Get list of all live blog posts"""
    blog_posts = BlogPostPage.objects.live().public().specific()
    result = []
    for post in blog_posts:
        authors = []
        for a in post.authors.all():
            author_dict = {'id': a.id, 'name': a.name, 'bio': a.bio}
            if getattr(a, 'image', None):
                try:
                    author_dict['image'] = request.build_absolute_uri(a.image.file.url)
                except Exception:
                    author_dict['image'] = a.image.file.url
            authors.append(author_dict)
        
        post_dict = {
            'id': post.id,
            'title': post.title,
            'date': post.date,
            'quote': _strip_html(post.quote),
            'intro': _strip_html(post.intro),
            'first_image': _abs_url(request, post.main_image().file.url) if post.main_image() else None,
            'authors': authors,
            'tags': [tag.name for tag in post.tags.all()],
            'slug': post.slug
        }
        post_dict = _add_first_image(request, post, post_dict)
        result.append(post_dict)
    return result

@router.get('/post/{slug}/', response=BlogPostDetailSchema)
def blog_detail(request, slug: str):
    blog_post = get_object_or_404(
        BlogPostPage.objects.live().public().specific().prefetch_related('authors', 'tags', 'gallery_images'), 
        slug=slug
    )
    
    # ✅ CRITICAL: Force JSON serialization before Pydantic validation
    body_json = blog_post.body.get_prep_value() if blog_post.body else []
    
    response = {
        'id': blog_post.id,
        'title': blog_post.title,
        'slug': blog_post.slug,
        'date': blog_post.date,
        'quote': _strip_html(blog_post.quote),
        'intro': _strip_html(blog_post.intro),  # ✅ Clean text only
        'body': _process_body_json(body_json), # ✅ Paragraphs stripped, headings clean
        'authors': [
            {
                'id': a.id, 
                'name': a.name,
                'bio': a.bio,
                'image': _abs_url(request, getattr(a, 'image', None).file.url) if getattr(a, 'image', None) else None
            }
            for a in blog_post.authors.all()
        ],
        'tags': [tag.name for tag in blog_post.tags.all()],
        'gallery_images': [
            {'image': _abs_url(request, g.image.file.url), 'caption': g.caption}
            for g in blog_post.gallery_images.all()
        ],
        'category': getattr(blog_post, 'category', None)
    }

    return response

@router.get('/post/{id}/', response=BlogPostDetailSchema)  # Use same schema as slug endpoint
def blog_detail_id(request, id: int):
    """Get single blog post by ID"""
    blog_post = get_object_or_404(
        BlogPostPage.objects.live().public().specific()
        .prefetch_related('authors', 'tags', 'gallery_images'), 
        id=id
    )
    
    # ✅ Force JSON serialization (fixes StreamValue error)
    body_json = blog_post.body.to_json_object() if blog_post.body else []
    
    # ✅ Complete dict transformation (not raw ORM object)
    response = {
        'id': blog_post.id,
        'title': blog_post.title,
        'slug': blog_post.slug,
        'date': blog_post.date,
        'quote': _strip_html(blog_post.quote),
        'intro': _strip_html(blog_post.intro),  # ✅ Clean text only
        'body': _process_body_json(body_json), # ✅ Paragraphs stripped, headings clean
        'authors': [
            {
                'id': a.id, 
                'name': a.name,
                'image': _abs_url(request, getattr(a, 'image', None).file.url) if getattr(a, 'image', None) else None
            }
            for a in blog_post.authors.all()
        ],
        'tags': [tag.name for tag in blog_post.tags.all()],
        'gallery_images': [
            {
                'image': _abs_url(request, g.image.file.url), 
                'caption': g.caption
            }
            for g in blog_post.gallery_images.all()
        ],
        'category': getattr(blog_post, 'category', None)
    }

    return response