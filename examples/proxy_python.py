from __future__ import annotations
from abc import ABC, abstractmethod


class Subject(ABC):
    """抽象主题：定义客户端期望的接口。"""

    @abstractmethod
    def request(self, user: str) -> str:
        pass


class RealSubject(Subject):
    """真实主题：真正执行操作的类。"""

    def request(self, user: str) -> str:
        # 模拟一项成本较高或敏感的操作
        return f"RealSubject: 为 {user} 处理请求。"


class Proxy(Subject):
    """代理：在客户端和真实主题之间控制访问、做缓存、记录等。"""

    def __init__(self, real_subject: RealSubject, allowed_users: set[str] | None = None):
        self._real = real_subject
        self._allowed = allowed_users or set()

    def _check_access(self, user: str) -> bool:
        # 简单访问控制示例
        return user in self._allowed

    def _log(self, message: str) -> None:
        print(f"[Proxy log] {message}")

    def request(self, user: str) -> str:
        self._log(f"收到来自 {user} 的请求")
        if not self._check_access(user):
            self._log(f"拒绝访问：{user}")
            return "Proxy: 拒绝访问"

        # 可以在调用真实主题前后做额外工作
        result = self._real.request(user)
        self._log(f"已为 {user} 完成请求")
        return result


def main() -> None:
    real = RealSubject()
    proxy = Proxy(real_subject=real, allowed_users={"alice", "bob"})

    for user in ("alice", "eve"):
        print(f"客户端: {user} 请求 ->", proxy.request(user))


if __name__ == "__main__":
    main()
