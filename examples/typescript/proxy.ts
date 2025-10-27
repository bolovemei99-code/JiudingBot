/**
 * TypeScript 代理模式示例（供参考）。
 * 运行方法（需先安装 node + ts-node 或编译为 JS）：
 *   npx ts-node proxy.ts
 */

interface Subject {
  request(user: string): string;
}

class RealSubject implements Subject {
  request(user: string): string {
    return `RealSubject: 为 ${user} 处理请求。`;
  }
}

class ProxyImpl implements Subject {
  private real: RealSubject;
  private allowed: Set<string>;

  constructor(real: RealSubject, allowed: Set<string>) {
    this.real = real;
    this.allowed = allowed;
  }

  private checkAccess(user: string): boolean {
    return this.allowed.has(user);
  }

  request(user: string): string {
    console.log(`[Proxy log] 收到来自 ${user} 的请求`);
    if (!this.checkAccess(user)) {
      console.log(`[Proxy log] 拒绝访问：${user}`);
      return 'Proxy: 拒绝访问';
    }
    const r = this.real.request(user);
    console.log(`[Proxy log] 已为 ${user} 完成请求`);
    return r;
  }
}

function main() {
  const real = new RealSubject();
  const proxy = new ProxyImpl(real, new Set(['alice', 'bob']));
  console.log(proxy.request('alice'));
  console.log(proxy.request('eve'));
}

if (require.main === module) main();
