from .cart import router as cart_router
from .catalog import router as catalog_router
from .faq import router as faq_router
from .start import router as start_router
from .product import router as product_router
from .order import router as order_router

routers = (start_router, order_router, product_router, cart_router, catalog_router, faq_router)

__all__ = [routers]
