import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path to import check_deployment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import check_deployment


class TestDeploymentChecks:
    """测试部署检查功能"""
    
    def test_validate_bot_token_valid(self):
        """测试有效的 Bot Token 格式"""
        valid_tokens = [
            "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
            "987654321:XYZ123abc456DEF789-_",
            "111111111:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p"
        ]
        for token in valid_tokens:
            assert check_deployment.validate_bot_token(token), f"Token {token} should be valid"
    
    def test_validate_bot_token_invalid(self):
        """测试无效的 Bot Token 格式"""
        invalid_tokens = [
            "",
            "not-a-token",
            "123456789",  # 缺少冒号和第二部分
            ":ABCdefGHI",  # 缺少数字部分
            "abc:123456",  # 第一部分不是数字
            "123:ABC DEF"  # 包含空格
        ]
        for token in invalid_tokens:
            assert not check_deployment.validate_bot_token(token), f"Token {token} should be invalid"
    
    def test_check_environment_variables_missing(self, monkeypatch):
        """测试环境变量缺失的情况"""
        # 清除环境变量
        monkeypatch.delenv('BOT_TOKEN', raising=False)
        monkeypatch.delenv('RAILWAY_TOKEN', raising=False)
        
        missing = check_deployment.check_environment_variables()
        assert len(missing) == 2
        assert any('BOT_TOKEN' in item for item in missing)
        assert any('RAILWAY_TOKEN' in item for item in missing)
    
    def test_check_environment_variables_present(self, monkeypatch):
        """测试环境变量存在的情况"""
        monkeypatch.setenv('BOT_TOKEN', '123456789:ABCdefGHIjklMNOpqrsTUVwxyz')
        monkeypatch.setenv('RAILWAY_TOKEN', 'test-railway-token')
        
        missing = check_deployment.check_environment_variables()
        assert len(missing) == 0
    
    def test_check_environment_variables_invalid_token(self, monkeypatch):
        """测试 Bot Token 格式无效的情况"""
        monkeypatch.setenv('BOT_TOKEN', 'invalid-token-format')
        monkeypatch.setenv('RAILWAY_TOKEN', 'test-railway-token')
        
        missing = check_deployment.check_environment_variables()
        assert len(missing) == 1
        assert 'BOT_TOKEN' in missing[0]
        assert '格式无效' in missing[0]
    
    def test_check_required_files(self, monkeypatch):
        """测试必需文件检查"""
        # 切换到临时目录
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            
            try:
                # 所有文件都不存在
                missing = check_deployment.check_required_files()
                assert len(missing) == 3
                
                # 创建文件
                Path('bot.py').touch()
                Path('requirements.txt').touch()
                Path('railway.json').touch()
                
                # 所有文件都存在
                missing = check_deployment.check_required_files()
                assert len(missing) == 0
            finally:
                os.chdir(original_dir)
    
    def test_check_dependencies(self, monkeypatch):
        """测试依赖检查"""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            
            try:
                # 创建有效的 requirements.txt
                with open('requirements.txt', 'w') as f:
                    f.write('python-telegram-bot==20.7\n')
                
                # 创建有效的 railway.json
                with open('railway.json', 'w') as f:
                    f.write('{"build": {}, "start": {"command": "python bot.py"}}')
                
                issues = check_deployment.check_dependencies()
                assert len(issues) == 0
                
                # 测试空的 requirements.txt
                with open('requirements.txt', 'w') as f:
                    f.write('')
                
                issues = check_deployment.check_dependencies()
                assert len(issues) == 1
                assert 'requirements.txt' in issues[0]
                
            finally:
                os.chdir(original_dir)
    
    def test_check_dependencies_invalid_json(self, monkeypatch):
        """测试无效的 railway.json"""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            
            try:
                # 创建有效的 requirements.txt
                with open('requirements.txt', 'w') as f:
                    f.write('python-telegram-bot==20.7\n')
                
                # 创建无效的 railway.json
                with open('railway.json', 'w') as f:
                    f.write('invalid json content')
                
                issues = check_deployment.check_dependencies()
                assert len(issues) == 1
                assert 'railway.json' in issues[0]
                assert 'JSON 格式无效' in issues[0] or '格式无效' in issues[0]
                
            finally:
                os.chdir(original_dir)
    
    def test_check_bot_configuration(self):
        """测试 bot.py 配置检查"""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            
            try:
                # 创建使用环境变量的 bot.py
                with open('bot.py', 'w') as f:
                    f.write('import os\ntoken = os.environ.get("BOT_TOKEN")\n')
                
                issues = check_deployment.check_bot_configuration()
                assert len(issues) == 0
                
                # 创建不使用环境变量的 bot.py
                with open('bot.py', 'w') as f:
                    f.write('token = "hardcoded-token"\n')
                
                issues = check_deployment.check_bot_configuration()
                assert len(issues) == 1
                
            finally:
                os.chdir(original_dir)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
