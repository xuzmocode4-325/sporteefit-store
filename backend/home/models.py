from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.blocks import ListBlock, CharBlock, StructBlock, RichTextBlock

from modelcluster.fields import ParentalKey
from wagtail_headless_preview.models import HeadlessPreviewMixin


class StatBlock(StructBlock):
    name = CharBlock(max_length=255, help_text="Stat name, e.g., 'Offices worldwide'")
    value = CharBlock(max_length=100, help_text="Stat value, e.g., '12' or '300+'")

    class Meta:
        icon = 'grip'
        template = 'blocks/stat_block.html'


class HomePage(HeadlessPreviewMixin, Page):
    """
    Home page model - add preview support.
    Assumes Vue route: "/"
    """

    headline = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)

    # Add other fields as needed

    content_panels = Page.content_panels + [
        FieldPanel('headline'),
        FieldPanel('body'),
    ]

    preview_url = "/"


class AboutPage(HeadlessPreviewMixin, Page):
    """
    About page model with stats block.
    Assumes Vue route: "/about"
    """
    headline = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    stats = StreamField(
        [('stat', StatBlock())],
        blank=True,
        use_json_field=True,
        help_text='Add key statistics (e.g., team size, experience). Orderable via drag-and-drop.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('headline'),
        FieldPanel('body'),
        FieldPanel('stats'),
    ]

    preview_url = "/about"

    class Meta:
        verbose_name = "About Page"


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('bio'),
        FieldPanel('image'),
    ]

    def __str__(self):
        return self.name


class ContactSubmission(models.Model):
    """Store contact form submissions"""
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=20)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"

    def __str__(self):
        return self.name
    