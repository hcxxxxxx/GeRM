import unittest
from unittest.mock import MagicMock, patch

from src.models.agent import ReadmeAgent
from config.config import Config

class TestReadmeAgent(unittest.TestCase):
    """测试ReadmeAgent类"""
    
    def setUp(self):
        # 设置测试前的准备工作
        self.agent = ReadmeAgent()
        
        # 模拟OpenAI客户端
        self.mock_openai_client_patcher = patch('src.models.agent.OpenAIClient')
        self.mock_openai_client = self.mock_openai_client_patcher.start()
        
        # 设置模拟的返回值
        self.mock_instance = self.mock_openai_client.return_value
        self.mock_instance.chat_completion.return_value = "测试README内容"
        
        # 替换agent的客户端为模拟对象
        self.agent.openai_client = self.mock_instance
    
    def tearDown(self):
        # 测试结束后的清理工作
        self.mock_openai_client_patcher.stop()
    
    def test_generate_readme(self):
        """测试README生成功能"""
        # 准备测试数据
        repo_analysis = {
            "repo_name": "test-repo",
            "languages": ["Python"],
            "structure": {"name": "test-repo", "type": "directory", "children": []}
        }
        
        # 调用被测试的方法
        result = self.agent.generate_readme(repo_analysis)
        
        # 验证结果
        self.assertEqual(result, "测试README内容")
        
        # 验证OpenAI客户端被正确调用
        self.mock_instance.chat_completion.assert_called_once()
        args, kwargs = self.mock_instance.chat_completion.call_args
        self.assertEqual(kwargs["system_prompt"], Config.SYSTEM_PROMPT)
    
    def test_analyze_code_file(self):
        """测试代码文件分析功能"""
        # 准备测试数据
        file_path = "test.py"
        file_content = "def hello(): print('Hello, World!')"
        
        # 设置模拟的JSON返回值
        self.mock_instance.chat_completion.return_value = '{"purpose": "测试函数", "components": ["hello"]}'
        
        # 调用被测试的方法
        result = self.agent.analyze_code_file(file_path, file_content)
        
        # 验证结果
        self.assertEqual(result["purpose"], "测试函数")
        self.assertEqual(result["components"], ["hello"])
        
        # 验证OpenAI客户端被正确调用
        self.mock_instance.chat_completion.assert_called_once()

if __name__ == '__main__':
    unittest.main()
