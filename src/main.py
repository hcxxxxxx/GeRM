import os
import sys
import logging
import click
from tqdm import tqdm
from typing import Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config
from src.services.code_analyzer import CodeAnalyzer
from src.services.readme_generator import ReadmeGenerator
from src.utils.file_handler import FileHandler

# 配置日志
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.command()
@click.option('--repo_path', required=True, help='要分析的代码仓库路径')
@click.option('--output', default=Config.DEFAULT_OUTPUT_FILENAME, help='输出README文件的名称')
@click.option('--model', default=None, help='要使用的OpenAI模型')
@click.option('--verbose', is_flag=True, help='显示详细日志')
def main(repo_path: str, output: str, model: Optional[str], verbose: bool):
    """根据代码仓库生成README.md文件的命令行工具"""
    try:
        # 验证配置
        Config.validate_config()
        
        # 设置详细日志
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # 如果提供了模型参数，覆盖配置
        if model:
            Config.OPENAI_MODEL = model
        
        logger.info(f"开始分析仓库: {repo_path}")
        
        # 分析代码仓库
        with tqdm(total=3, desc="生成README") as pbar:
            pbar.set_description("分析代码仓库")
            code_analyzer = CodeAnalyzer(repo_path)
            repo_analysis = code_analyzer.analyze()
            pbar.update(1)
            
            pbar.set_description("生成README内容")
            readme_generator = ReadmeGenerator()
            readme_content = readme_generator.generate(repo_analysis)
            pbar.update(1)
            
            pbar.set_description("保存README文件")
            output_path = os.path.join(repo_path, output)
            FileHandler.write_file(output_path, readme_content)
            pbar.update(1)
        
        logger.info(f"README生成完成，已保存到: {output_path}")
        
    except Exception as e:
        logger.error(f"生成README时出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
