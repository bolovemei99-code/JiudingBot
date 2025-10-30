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

## 部署检查

在部署到生产环境之前，应该运行部署条件检查以确保所有必需的配置都已正确设置。

### 运行部署检查

```bash
# 使用 Python 直接运行
python check_deployment.py

# 或使用 Makefile
make check-deploy
```

### 检查内容

部署检查脚本会验证以下条件：

1. **环境变量检查**
   - `BOT_TOKEN`: Telegram Bot 认证令牌
   - `RAILWAY_TOKEN`: Railway 部署令牌

2. **必需文件检查**
   - `bot.py`: 主程序文件
   - `requirements.txt`: Python 依赖
   - `railway.json`: Railway 配置

3. **依赖配置检查**
   - requirements.txt 不为空
   - railway.json 格式正确且包含必需配置

4. **Bot 配置检查**
   - 验证 bot.py 使用环境变量
   - 检查是否存在硬编码的敏感信息

### CI/CD 集成

部署检查已集成到 `.github/workflows/ci-cd.yml` 中，在实际部署前自动运行。如果检查失败，部署将被中止。

