#!/usr/bin/env python3
"""
部署前检查脚本 (Pre-deployment check script)
检查部署所需的所有条件是否满足
"""
import os
import sys
import re


def check_environment_variables():
    """检查必需的环境变量是否存在"""
    print("检查环境变量...")
    required_vars = {
        'BOT_TOKEN': '用于 Telegram Bot 认证',
        'RAILWAY_TOKEN': '用于 Railway 部署'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if not value:
            missing_vars.append(f"  - {var}: {description}")
            print(f"  ❌ {var} 未设置")
        else:
            # 验证 token 格式（不显示完整 token）
            if var == 'BOT_TOKEN':
                if not validate_bot_token(value):
                    missing_vars.append(f"  - {var}: Token 格式无效")
                    print(f"  ❌ {var} 格式无效")
                else:
                    print(f"  ✓ {var} 已设置且格式正确")
            else:
                print(f"  ✓ {var} 已设置")
    
    return missing_vars


def validate_bot_token(token):
    """验证 Telegram Bot Token 格式"""
    # Telegram bot token 格式: 数字:字母数字字符串
    # 例如: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
    pattern = r'^\d+:[A-Za-z0-9_-]+$'
    return re.match(pattern, token) is not None


def check_required_files():
    """检查必需的文件是否存在"""
    print("\n检查必需文件...")
    required_files = [
        'bot.py',
        'requirements.txt',
        'railway.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(f"  - {file}")
            print(f"  ❌ {file} 不存在")
        else:
            print(f"  ✓ {file} 存在")
    
    return missing_files


def check_dependencies():
    """检查依赖文件内容是否有效"""
    print("\n检查依赖配置...")
    issues = []
    
    # 检查 requirements.txt
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            content = f.read().strip()
            if not content:
                issues.append("  - requirements.txt 为空")
                print("  ❌ requirements.txt 为空")
            else:
                print("  ✓ requirements.txt 包含依赖")
    
    # 检查 railway.json
    if os.path.exists('railway.json'):
        try:
            import json
            with open('railway.json', 'r') as f:
                config = json.load(f)
                if 'build' not in config or 'start' not in config:
                    issues.append("  - railway.json 缺少必需的 build 或 start 配置")
                    print("  ❌ railway.json 配置不完整")
                else:
                    print("  ✓ railway.json 配置完整")
        except json.JSONDecodeError:
            issues.append("  - railway.json 格式无效")
            print("  ❌ railway.json JSON 格式无效")
    
    return issues


def check_bot_configuration():
    """检查 bot.py 配置"""
    print("\n检查 Bot 配置...")
    issues = []
    
    if os.path.exists('bot.py'):
        with open('bot.py', 'r') as f:
            content = f.read()
            
            # 检查是否使用环境变量
            if 'os.environ.get' not in content and 'BOT_TOKEN' not in content:
                issues.append("  - bot.py 未使用环境变量获取 BOT_TOKEN")
                print("  ❌ bot.py 未正确使用环境变量")
            else:
                print("  ✓ bot.py 使用环境变量")
            
            # 检查是否有硬编码的 token (只是警告)
            token_pattern = r'\d{10}:\w{35}'
            if re.search(token_pattern, content):
                print("  ⚠️  警告: bot.py 中可能包含硬编码的 token")
                print("     (这是一个安全风险，应该只使用环境变量)")
    
    return issues


def main():
    """主函数：执行所有部署前检查"""
    print("=" * 60)
    print("开始部署条件检查...")
    print("=" * 60)
    
    all_issues = []
    
    # 执行各项检查
    env_issues = check_environment_variables()
    file_issues = check_required_files()
    dep_issues = check_dependencies()
    config_issues = check_bot_configuration()
    
    # 汇总所有问题
    all_issues.extend(env_issues)
    all_issues.extend(file_issues)
    all_issues.extend(dep_issues)
    all_issues.extend(config_issues)
    
    print("\n" + "=" * 60)
    if all_issues:
        print("❌ 部署条件检查失败！")
        print("\n发现以下问题：")
        for issue in all_issues:
            print(issue)
        print("\n请解决上述问题后再进行部署。")
        print("=" * 60)
        return 1
    else:
        print("✓ 所有部署条件检查通过！")
        print("可以安全部署。")
        print("=" * 60)
        return 0


if __name__ == '__main__':
    sys.exit(main())
