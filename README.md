# JiudingBot

[![CI](https://github.com/bolovemei99-code/JiudingBot/actions/workflows/ci.yml/badge.svg)](https://github.com/bolovemei99-code/JiudingBot/actions/workflows/ci.yml)

## 代理模式（Proxy Pattern）示例

仓库新增了一个代理模式示例集合，路径：`examples/`

- `examples/proxy_python.py`：Python 可运行示例（包含访问控制与简单日志）。
- `examples/java/ProxyExample.java`：Java 参考实现（可用 javac/java 运行）。
- `examples/typescript/proxy.ts`：TypeScript 参考实现（可用 ts-node 运行）。

TypeScript 运行说明（在 `examples/typescript` 目录下）：

```bash
cd examples/typescript
npm install
# 运行示例
npm run start
```

如何运行 Python 示例与测试：

1. 安装依赖（推荐使用虚拟环境）：

```bash
pip install -r requirements.txt
```

2. 运行示例：

```bash
python examples/proxy_python.py
```

3. 运行测试（使用 pytest）：

```bash
pytest -q
```

更多说明见 `examples/` 中的文件注释。

### 运行 TypeScript 示例

如果你想运行 TypeScript 示例（`examples/typescript/proxy.ts`），请进入该目录并安装依赖：

```bash
cd examples/typescript
npm install
```

然后运行：

```bash
npm run start
# 或使用 npx：
npx ts-node proxy.ts
```

### 缓存代理示例（Python）

新增 `examples/proxy_python_cache.py`，演示如何用代理做本地缓存以减少对真实对象的重复调用。

运行示例：

```bash
python examples/proxy_python_cache.py
```

