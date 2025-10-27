from __future__ import annotations
from abc import ABC, abstractmethod
import time


class Subject(ABC):
    @abstractmethod
    def request(self, key: str) -> str:
        pass


class RealSubjectWithCounter(Subject):
    """真实主题，包含计数器以便测试缓存命中率。"""

    def __init__(self) -> None:
        self.call_count = 0

    def request(self, key: str) -> str:
        # 模拟昂贵计算或远程请求
        time.sleep(0.01)
        self.call_count += 1
        return f"Real: result for {key} (call {self.call_count})"


class CacheProxy(Subject):
    """简单缓存代理：按 key 缓存结果，减少对真实对象的重复调用。"""

    def __init__(self, real: RealSubjectWithCounter) -> None:
        self._real = real
        self._cache: dict[str, str] = {}

    def request(self, key: str) -> str:
        if key in self._cache:
            # 缓存命中
            return self._cache[key]

        # 缓存未命中，调用真实对象并缓存
        result = self._real.request(key)
        self._cache[key] = result
        return result

    def clear_cache(self) -> None:
        self._cache.clear()


def main() -> None:
    real = RealSubjectWithCounter()
    proxy = CacheProxy(real)

    print(proxy.request("a"))
    print(proxy.request("a"))  # 应从缓存返回
    print(proxy.request("b"))
    print(f"真实调用次数: {real.call_count}")


if __name__ == "__main__":
    main()
