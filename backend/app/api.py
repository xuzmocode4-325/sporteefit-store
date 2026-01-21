import logging
from ninja_extra import NinjaExtraAPI
from cart.api import router as cart_router
from store.api import router as product_router
from accounts.api import router as accounts_router
from payments.api import router as payments_router
from home.api import router as home_router
from blog.api import router as blog_router

logger = logging.getLogger(__name__)

api = NinjaExtraAPI(csrf=True)

api.add_router("/accounts", accounts_router)
api.add_router("/store", product_router)
api.add_router("/cart", cart_router)
api.add_router("/payments", payments_router)
api.add_router("/home", home_router)
api.add_router("/blog", blog_router)