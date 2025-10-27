from examples.proxy_python_cache import RealSubjectWithCounter, CacheProxy


def test_cache_reduces_real_calls():
    real = RealSubjectWithCounter()
    proxy = CacheProxy(real)

    # 第一次请求 a，会调用真实对象
    r1 = proxy.request("a")
    # 第二次请求 a，应走缓存，不增加真实调用次数
    r2 = proxy.request("a")
    # 请求 b，会触发新的真实调用
    r3 = proxy.request("b")

    assert r1 == r2
    assert "result for a" in r1
    assert "result for b" in r3
    assert real.call_count == 2


def test_clear_cache_allows_recall():
    real = RealSubjectWithCounter()
    proxy = CacheProxy(real)

    proxy.request("x")
    assert real.call_count == 1
    proxy.clear_cache()
    proxy.request("x")
    assert real.call_count == 2
