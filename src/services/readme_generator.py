import os
import logging
from typing import Dict, Any

from src.models.agent import ReadmeAgent

logger = logging.getLogger(__name__)

class ReadmeGenerator:
    """README生成服务类"""
    
    def __init__(self):
        """初始化README生成器"""
        self.agent = ReadmeAgent()
    
    def generate(self, repo_analysis: Dict[str, Any]) -> str:
        """
        根据仓库分析结果生成README
        
        Args:
            repo_analysis: 仓库分析结果
            
        Returns:
            str: 生成的README内容
        """
        logger.info("开始生成README内容")
        
        try:
            # 预处理分析结果
            processed_analysis = self._preprocess_analysis(repo_analysis)
            
            # 使用Agent生成README
            readme_content = self.agent.generate_readme(processed_analysis)
            
            # 去掉开头的```markdown标识头
            if readme_content.startswith("```markdown"):
                readme_content = readme_content.replace("```markdown", "", 1).strip()
            if readme_content.endswith("```"):
                readme_content = readme_content[:-3].strip()
            
            logger.info("README生成成功")
            return readme_content
            
        except Exception as e:
            logger.error(f"生成README失败: {str(e)}")
            raise
    
    def _preprocess_analysis(self, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        预处理仓库分析结果
        
        Args:
            repo_analysis: 原始仓库分析结果
            
        Returns:
            Dict[str, Any]: 处理后的分析结果
        """
        processed = repo_analysis.copy()
        
        # 如果languages是集合，转换为列表
        if isinstance(processed.get("languages"), set):
            processed["languages"] = list(processed["languages"])
        
        # 提取最重要的文件分析结果
        if "files_analysis" in processed:
            important_files = {}
            for path, analysis in processed["files_analysis"].items():
                # 只保留分析结果，不包含文件内容
                important_files[path] = {
                    "language": analysis.get("language", "Unknown"),
                    "summary": analysis.get("analysis", {}).get("purpose", "")
                }
            processed["important_files"] = important_files
        
        # 确保依赖格式一致
        if "dependencies" in processed:
            # 处理依赖信息，确保格式一致
            pass
        
        # 添加仓库名称和路径
        if "repo_name" not in processed:
            processed["repo_name"] = "Unknown Project"
        
        return processed
