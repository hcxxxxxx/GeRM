import unittest
import os
from unittest.mock import MagicMock, patch
import tempfile
import shutil

from src.services.code_analyzer import CodeAnalyzer

class TestCodeAnalyzer(unittest.TestCase):
    """测试CodeAnalyzer类"""
    
    def setUp(self):
        # 创建临时目录作为测试仓库
        self.test_repo_path = tempfile.mkdtemp()
        
        # 在临时目录中创建一些测试文件
        with open(os.path.join(self.test_repo_path, "test.py"), "w") as f:
            f.write("def test(): pass")
            
        with open(os.path.join(self.test_repo_path, "README.md"), "w") as f:
            f.write("# Test Repository")
            
        with open(os.path.join(self.test_repo_path, "requirements.txt"), "w") as f:
            f.write("pytest==7.0.0")
            
        # 创建一个子目录和文件
        os.makedirs(os.path.join(self.test_repo_path, "src"), exist_ok=True)
        with open(os.path.join(self.test_repo_path, "src", "main.py"), "w") as f:
            f.write("def main(): print('Hello')")
        
        # 创建应忽略的目录和文件
        os.makedirs(os.path.join(self.test_repo_path, "__pycache__"), exist_ok=True)
        with open(os.path.join(self.test_repo_path, "__pycache__", "test.cpython-39.pyc"), "w") as f:
            f.write("# Compiled Python file")
        
        # 模拟ReadmeAgent
        self.mock_agent_patcher = patch('src.services.code_analyzer.ReadmeAgent')
        self.mock_agent = self.mock_agent_patcher.start()
        
        # 设置模拟的返回值
        self.mock_instance = self.mock_agent.return_value
        self.mock_instance.analyze_code_file.return_value = {"purpose": "Test purpose"}
        
        # 初始化代码分析器
        self.analyzer = CodeAnalyzer(self.test_repo_path)
        self.analyzer.agent = self.mock_instance
    
    def tearDown(self):
        # 清理临时目录
        shutil.rmtree(self.test_repo_path)
        
        # 停止模拟
        self.mock_agent_patcher.stop()
    
    def test_analyze(self):
        """测试代码仓库分析功能"""
        # 调用被测试的方法
        result = self.analyzer.analyze()
        
        # 验证结果
        self.assertEqual(result["repo_name"], os.path.basename(self.test_repo_path))
        self.assertIn("Python", result["languages"])
        self.assertIn("README.md", result["key_files"])
        self.assertIn("requirements.txt", result["key_files"])
        
        # 验证结构包含正确的目录和文件
        structure = result["structure"]
        self.assertEqual(structure["name"], os.path.basename(self.test_repo_path))
        self.assertEqual(structure["type"], "directory")
        
        # 验证忽略的目录不在结构中
        children_names = [child["name"] for child in structure["children"]]
        self.assertIn("src", children_names)
        self.assertIn("test.py", children_names)
        self.assertNotIn("__pycache__", children_names)
        
        # 验证代理被调用来分析文件
        self.mock_instance.analyze_code_file.assert_called()

if __name__ == '__main__':
    unittest.main()
