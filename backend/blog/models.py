from django import forms
from django.db import models
from datetime import date

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import StructBlock, CharBlock, ChoiceBlock, RichTextBlock
from wagtail.admin.panels import FieldPanel, InlinePanel

from wagtail_headless_preview.models import HeadlessPreviewMixin

from taggit.models import TaggedItemBase
from modelcluster.models import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager



class BlogTag(TaggedItemBase):
    content_object = ParentalKey(
        'blog.BlogPostPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogIndexPage(HeadlessPreviewMixin, Page):
    """
    Blog listing index page.
    Assumes Vue route: "/blog/"
    """
    description = RichTextField(blank=True, features=['h2', 'bold', 'italic', 'link'])

    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

    preview_url = "/blog/"


class BlogPostPage(HeadlessPreviewMixin, Page):
    """
    Blog post detail - already had mixin, updated preview_url.
    Assumes Vue route: "/blog/{slug}/"
    """
    date = models.DateField('Post date', default=date.today)
    quote = RichTextField(blank=True, features=['h3', 'italic', 'bold', 'link'])
    intro = RichTextField(blank=True, features=['h2', 'bold', 'italic', 'link'])
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField('home.Author', blank=True)
    category = models.CharField(max_length=100, blank=True)
    tags = ClusterTaggableManager(through=BlogTag, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel('gallery_images', label="Gallery images"),
        FieldPanel('date'),
        FieldPanel('quote'),
        FieldPanel('intro'),      
        FieldPanel('body'),
        FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tags'),
    ]

    preview_url = "/blog/preview/"  # Preview route in Vue (with token param)

    def main_image(self):
        first_image = self.gallery_images.first()
        if first_image:
            return first_image.image
        return None


class BlogPageImageGallery(Orderable):
    page = ParentalKey(
        BlogPostPage, on_delete=models.CASCADE, related_name='gallery_images'
    )
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]