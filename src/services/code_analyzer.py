import os
import logging
from typing import Dict, List, Any, Set

from src.utils.code_parser import CodeParser
from src.utils.file_handler import FileHandler
from src.models.agent import ReadmeAgent

logger = logging.getLogger(__name__)

class CodeAnalyzer:
    """代码分析服务类"""
    
    # 关键文件名，用于优先分析
    KEY_FILES = {
        'README.md', 'package.json', 'setup.py', 'requirements.txt',
        'Pipfile', 'pyproject.toml', 'Makefile', 'Dockerfile',
        'docker-compose.yml', '.gitignore', 'LICENSE', 'CONTRIBUTING.md'
    }
    
    # 分析的最大文件数
    MAX_FILES_TO_ANALYZE = 20
    
    def __init__(self, repo_path: str):
        """
        初始化代码分析器
        
        Args:
            repo_path: 代码仓库路径
        """
        self.repo_path = repo_path
        self.agent = ReadmeAgent()
    
    def analyze(self) -> Dict[str, Any]:
        """
        分析代码仓库
        
        Returns:
            Dict[str, Any]: 包含仓库分析结果的字典
        """
        logger.info(f"开始分析代码仓库: {self.repo_path}")
        
        # 检查路径是否存在
        if not os.path.exists(self.repo_path):
            raise ValueError(f"仓库路径不存在: {self.repo_path}")
        
        # 初始化分析结果
        analysis_result = {
            "repo_name": os.path.basename(self.repo_path),
            "structure": {},
            "files_analysis": {},
            "dependencies": {},
            "languages": set(),
            "key_files": {},
        }
        
        try:
            # 获取仓库结构
            analysis_result["structure"] = FileHandler.get_repo_structure(
                self.repo_path, 
                ignore_func=CodeParser.should_ignore
            )
            
            # 列出所有文件
            all_files = FileHandler.list_files(
                self.repo_path, 
                ignore_func=CodeParser.should_ignore
            )
            
            # 识别依赖
            analysis_result["dependencies"] = CodeParser.identify_dependencies(self.repo_path)
            
            # 分析关键文件
            self._analyze_key_files(all_files, analysis_result)
            
            # 分析代表性文件
            self._analyze_representative_files(all_files, analysis_result)
            
            # 转换语言集合为列表
            analysis_result["languages"] = list(analysis_result["languages"])
            
            logger.info(f"代码仓库分析完成，识别到 {len(analysis_result['languages'])} 种语言，分析了 {len(analysis_result['files_analysis'])} 个文件")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"分析代码仓库失败: {str(e)}")
            raise
    
    def _analyze_key_files(self, all_files: List[str], analysis_result: Dict[str, Any]) -> None:
        """
        分析关键文件
        
        Args:
            all_files: 所有文件路径列表
            analysis_result: 分析结果字典
        """
        # 查找关键文件
        key_files = []
        for file_path in all_files:
            file_name = os.path.basename(file_path)
            if file_name in self.KEY_FILES:
                key_files.append(file_path)
        
        # 读取关键文件内容
        for file_path in key_files:
            rel_path = os.path.relpath(file_path, self.repo_path)
            file_content = FileHandler.read_file(file_path)
            
            # 添加到关键文件字典
            analysis_result["key_files"][rel_path] = file_content
            
            # 特殊处理README.md，如果存在的话
            if os.path.basename(file_path) == 'README.md':
                analysis_result["existing_readme"] = file_content
    
    def _analyze_representative_files(self, all_files: List[str], analysis_result: Dict[str, Any]) -> None:
        """
        分析代表性文件
        
        Args:
            all_files: 所有文件路径列表
            analysis_result: 分析结果字典
        """
        # 按文件类型分组
        files_by_extension = {}
        for file_path in all_files:
            _, ext = os.path.splitext(file_path)
            if ext not in files_by_extension:
                files_by_extension[ext] = []
            files_by_extension[ext].append(file_path)
        
        # 选择每种类型的代表性文件
        representative_files = []
        for ext, files in files_by_extension.items():
            # 跳过不受支持的扩展名
            if ext not in CodeParser.SUPPORTED_EXTENSIONS:
                continue
                
            # 根据文件大小和路径深度选择代表性文件
            # 优先选择较小且路径较浅的文件
            sorted_files = sorted(
                files,
                key=lambda f: (
                    os.path.getsize(f),  # 文件大小
                    len(f.split(os.sep))  # 路径深度
                )
            )
            
            # 每种类型最多选择3个文件
            representative_files.extend(sorted_files[:3])
        
        # 限制分析的文件总数
        representative_files = representative_files[:self.MAX_FILES_TO_ANALYZE]
        
        # 分析代表性文件
        for file_path in representative_files:
            rel_path = os.path.relpath(file_path, self.repo_path)
            
            # 如果已经在关键文件中，跳过
            if rel_path in analysis_result["key_files"]:
                continue
                
            # 读取文件内容
            file_content = FileHandler.read_file(file_path)
            
            # 识别语言
            language = CodeParser.identify_language(file_path)
            if language != 'Unknown':
                analysis_result["languages"].add(language)
            
            # 使用Agent分析文件
            file_analysis = self.agent.analyze_code_file(rel_path, file_content)
            
            # 添加到分析结果
            analysis_result["files_analysis"][rel_path] = {
                "language": language,
                "analysis": file_analysis,
                "size": len(file_content)
            }
