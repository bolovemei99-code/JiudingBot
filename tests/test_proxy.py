import pytest
from examples.proxy_python import RealSubject, Proxy


def test_proxy_allows_authorized_user(capsys):
    real = RealSubject()
    proxy = Proxy(real_subject=real, allowed_users={"alice"})

    res = proxy.request("alice")
    captured = capsys.readouterr()
    assert "拒绝访问" not in res
    assert "RealSubject" in res
    assert "收到来自 alice 的请求" in captured.out


def test_proxy_denies_unauthorized_user(capsys):
    real = RealSubject()
    proxy = Proxy(real_subject=real, allowed_users={"alice"})

    res = proxy.request("eve")
    captured = capsys.readouterr()
    assert res == "Proxy: 拒绝访问"
    assert "拒绝访问：eve" in captured.out
