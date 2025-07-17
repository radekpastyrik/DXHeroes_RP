# SDK public interface
from .client import OffersClient
from .models import Product, Offer
from .exceptions import OffersAPIError
from .retry import RetryConfig, AGGRESSIVE_RETRY, CONSERVATIVE_RETRY, FAST_RETRY

__all__ = [
    "OffersClient", 
    "Product", 
    "Offer", 
    "OffersAPIError",
    "RetryConfig",
    "AGGRESSIVE_RETRY",
    "CONSERVATIVE_RETRY", 
    "FAST_RETRY"
]
