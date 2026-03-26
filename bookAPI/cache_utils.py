from hashlib import sha256

from django.core.cache import cache


CACHE_VERSION_KEY = "book_list_cache_version"
BOOK_LIST_CACHE_TTL_SECONDS = 300


def _to_int(value, fallback):
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _to_sort_tokens(ordering_raw):
    if not ordering_raw:
        return ()
    return tuple(token.strip() for token in ordering_raw.split(",") if token.strip())


def normalize_list_params(params):
    category = params.get("category")
    price_from = params.get("price_from")
    price_to = params.get("price_to")
    ordering = params.get("ordering")

    # Small, deterministic payload to build a stable cache key.
    normalized = {
        "category": str(category) if category is not None else "",
        "price_from": str(price_from) if price_from is not None else "",
        "price_to": str(price_from) if price_to is not None else "",
        "ordering": _to_sort_tokens(ordering),
        "page": _to_int(params.get("page"), 1),
        "perpage": _to_int(params.get("perpage"), 10),
    }
    return normalized


def get_cache_version():
    version = cache.get(CACHE_VERSION_KEY)
    if version is None:
        version = 1
        cache.set(CACHE_VERSION_KEY, version, None)
    return version


def bump_cache_version():
    try:
        cache.incr(CACHE_VERSION_KEY)
    except ValueError:
        cache.set(CACHE_VERSION_KEY, 2, None)


def build_book_list_cache_key(normalized_params):
    version = get_cache_version()
    fingerprint = sha256(str(normalized_params).encode("utf-8")).hexdigest()
    return f"book_list:v{version}:{fingerprint}"
