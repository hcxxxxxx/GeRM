import logging
from typing import Dict, Any, List

from src.api.openai_client import OpenAIClient
from src.utils.prompt_templates import PromptTemplates
from config.config import Config

logger = logging.getLogger(__name__)

class ReadmeAgent:
    """基于LLM的README生成Agent"""
    
    def __init__(self):
        """初始化README生成Agent"""
        self.openai_client = OpenAIClient()
        self.system_prompt = Config.SYSTEM_PROMPT
    
    def generate_readme(self, repo_analysis: Dict[str, Any]) -> str:
        """
        生成README内容
        
        Args:
            repo_analysis: 包含代码仓库分析结果的字典
            
        Returns:
            str: 生成的README内容
        """
        logger.info("开始生成README内容")
        
        # 构建用户提示词
        user_prompt = PromptTemplates.get_readme_generation_prompt(repo_analysis)
        
        # 调用OpenAI API生成README
        try:
            readme_content = self.openai_client.chat_completion(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt
            )
            
            logger.info("README内容生成成功")
            return readme_content
            
        except Exception as e:
            logger.error(f"生成README内容失败: {str(e)}")
            raise
    
    def analyze_code_file(self, file_path: str, file_content: str) -> Dict[str, Any]:
        """
        分析单个代码文件
        
        Args:
            file_path: 文件路径
            file_content: 文件内容
            
        Returns:
            Dict[str, Any]: 文件分析结果
        """
        logger.debug(f"分析代码文件: {file_path}")
        
        # 构建文件分析提示词
        user_prompt = PromptTemplates.get_file_analysis_prompt(file_path, file_content)
        
        # 调用OpenAI API分析文件
        try:
            analysis_result = self.openai_client.chat_completion(
                system_prompt="你是一个代码分析专家，请分析以下代码文件并提取关键信息。",
                user_prompt=user_prompt,
                temperature=0.3  # 降低温度以获得更精确的分析
            )
            
            # 解析分析结果
            try:
                import json
                analysis_dict = json.loads(analysis_result)
                return analysis_dict
            except json.JSONDecodeError:
                # 如果无法解析为JSON，直接返回文本
                return {"summary": analysis_result}
                
        except Exception as e:
            logger.error(f"分析代码文件失败: {str(e)}")
            return {"error": str(e)}
