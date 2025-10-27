/**
 * 简单的 Java 代理模式示例（供参考）。
 * 编译与运行：javac ProxyExample.java && java ProxyExample
 */
interface Subject {
    String request(String user);
}

class RealSubject implements Subject {
    public String request(String user) {
        return "RealSubject: 为 " + user + " 处理请求。";
    }
}

class Proxy implements Subject {
    private RealSubject real;
    private java.util.Set<String> allowed;

    public Proxy(RealSubject real, java.util.Set<String> allowed) {
        this.real = real;
        this.allowed = allowed;
    }

    private boolean checkAccess(String user) {
        return allowed.contains(user);
    }

    private void log(String msg) {
        System.out.println("[Proxy log] " + msg);
    }

    public String request(String user) {
        log("收到来自 " + user + " 的请求");
        if (!checkAccess(user)) {
            log("拒绝访问：" + user);
            return "Proxy: 拒绝访问";
        }
        String result = real.request(user);
        log("已为 " + user + " 完成请求");
        return result;
    }
}

public class ProxyExample {
    public static void main(String[] args) {
        RealSubject real = new RealSubject();
        java.util.Set<String> allowed = new java.util.HashSet<>();
        allowed.add("alice");
        Proxy proxy = new Proxy(real, allowed);

        System.out.println(proxy.request("alice"));
        System.out.println(proxy.request("eve"));
    }
}
