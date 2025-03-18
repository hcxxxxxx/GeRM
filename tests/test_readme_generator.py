import unittest
from unittest.mock import MagicMock, patch

from src.services.readme_generator import ReadmeGenerator

class TestReadmeGenerator(unittest.TestCase):
    """测试ReadmeGenerator类"""
    
    def setUp(self):
        # 设置测试前的准备工作
        self.generator = ReadmeGenerator()
        
        # 模拟ReadmeAgent
        self.mock_agent_patcher = patch('src.services.readme_generator.ReadmeAgent')
        self.mock_agent = self.mock_agent_patcher.start()
        
        # 设置模拟的返回值
        self.mock_instance = self.mock_agent.return_value
        self.mock_instance.generate_readme.return_value = "# 测试项目\n\n这是一个测试项目的README。"
        
        # 替换generator的agent为模拟对象
        self.generator.agent = self.mock_instance
        
        # 准备测试数据
        self.test_repo_analysis = {
            "repo_name": "test-project",
            "languages": set(["Python", "Markdown"]),
            "structure": {"name": "test-project", "type": "directory", "children": []},
            "files_analysis": {
                "test.py": {
                    "language": "Python",
                    "analysis": {"purpose": "测试文件"},
                    "size": 100
                }
            },
            "key_files": {
                "README.md": "# Old README"
            },
            "dependencies": {
                "requirements.txt": "pytest==7.0.0"
            }
        }
    
    def tearDown(self):
        # 测试结束后的清理工作
        self.mock_agent_patcher.stop()
    
    def test_generate(self):
        """测试README生成功能"""
        # 调用被测试的方法
        result = self.generator.generate(self.test_repo_analysis)
        
        # 验证结果
        self.assertEqual(result, "# 测试项目\n\n这是一个测试项目的README。")
        
        # 验证预处理和代理调用
        self.mock_instance.generate_readme.assert_called_once()
        
        # 验证传递给代理的预处理数据
        args, kwargs = self.mock_instance.generate_readme.call_args
        processed_analysis = args[0]
        
        # 验证预处理转换了语言集合为列表
        self.assertIsInstance(processed_analysis["languages"], list)
        self.assertEqual(set(processed_analysis["languages"]), set(["Python", "Markdown"]))
        
        # 验证重要文件被提取
        self.assertIn("important_files", processed_analysis)
        self.assertIn("test.py", processed_analysis["important_files"])
        self.assertEqual(
            processed_analysis["important_files"]["test.py"]["language"], 
            "Python"
        )

if __name__ == '__main__':
    unittest.main()
