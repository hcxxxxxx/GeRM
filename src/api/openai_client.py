import logging
from typing import Dict, Any, List
from openai import OpenAI

from config.config import Config

logger = logging.getLogger(__name__)

class OpenAIClient:
    """OpenAI API客户端类"""
    
    def __init__(self):
        """初始化OpenAI客户端"""
        self.client = OpenAI(base_url="https://api.gptsapi.net/v1", api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
    
    def chat_completion(
        self, 
        system_prompt: str, 
        user_prompt: str,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        发送请求到OpenAI Chat Completion API
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            temperature: 温度参数，控制输出的随机性
            max_tokens: 生成的最大token数
            
        Returns:
            str: 模型生成的响应文本
        """
        if temperature is None:
            temperature = self.temperature
            
        if max_tokens is None:
            max_tokens = self.max_tokens
        
        try:
            logger.debug(f"发送请求到OpenAI API，模型: {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # 提取生成的文本
            generated_text = response.choices[0].message.content
            
            logger.debug(f"成功从OpenAI API获取响应，长度: {len(generated_text)}")
            return generated_text
            
        except Exception as e:
            logger.error(f"OpenAI API调用失败: {str(e)}")
            raise
