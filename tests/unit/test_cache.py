from cmt.services.cache import Cache


def test_create_cache_dir(cache_dir):
    assert not cache_dir.exists()

    Cache()

    assert cache_dir.is_dir()


def test_get_returns_none_when_missing(cache_dir):
    assert Cache().get("fake_key") is None


def test_set_then_get(cache_dir):
    cache = Cache()

    cache.set("author", "bijaydas")

    assert cache.get("author") == "bijaydas"


def test_different_keys_do_not_collide(cache_dir):
    cache = Cache()

    cache.set("a", "1")
    cache.set("b", "2")

    assert cache.get("a") == "1"
    assert cache.get("b") == "2"
