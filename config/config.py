import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # OpenAI API配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # 模型参数
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 4096))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
    
    # 应用配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # 输出配置
    DEFAULT_OUTPUT_FILENAME = "README.md"
    
    # 提示词配置
    SYSTEM_PROMPT = """你是一个专业的README文档生成器。你的任务是分析代码仓库，
    并生成一个全面、专业的README.md文件。关注项目的主要功能、安装步骤、使用方法、
    技术栈和架构。确保README清晰、结构良好并提供足够的细节帮助用户理解和使用项目。"""
    
    @classmethod
    def validate_config(cls):
        """验证配置是否有效"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY未设置，请在.env文件中配置")
        
        return True
