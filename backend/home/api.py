# backend/home/api.py
from ninja import Router
from typing import List
from .models import HomePage
from .schemas import HomePageSchema

router = Router(tags=["Home"])


@router.get("/", response=HomePageSchema)
def get_home_page(request):
    """Fetch the home page content"""
    home_page = HomePage.objects.live().first()
    if not home_page:
        return 404, {"detail": "Home page not found"}
    return home_page