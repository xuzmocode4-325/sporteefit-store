# backend/home/schemas.py
from ninja import ModelSchema
from .models import HomePage


class HomePageSchema(ModelSchema):
    class Meta:
        model = HomePage
        fields = ['id', 'title', 'slug', 'headline', 'body']