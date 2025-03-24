import os
import logging
from typing import Dict, List, Any, Set
from collections import Counter
import re

from src.utils.code_parser import CodeParser
from src.utils.file_handler import FileHandler
from src.models.agent import ReadmeAgent

logger = logging.getLogger(__name__)

class CodeAnalyzer:
    """代码分析服务类"""
    
    # 关键文件名，用于优先分析，但排除README.md
    KEY_FILES = {
        'package.json', 'setup.py', 'requirements.txt',
        'Pipfile', 'pyproject.toml', 'Makefile', 'Dockerfile',
        'docker-compose.yml', '.gitignore', 'LICENSE', 'CONTRIBUTING.md'
    }
    
    # 核心文件指标权重
    WEIGHTS = {
        'imports': 3,      # 被导入次数权重
        'size': 0.5,       # 文件大小权重(KB)
        'commits': 2,      # 提交历史中的修改次数
        'depth': -1,       # 目录深度（负值，越浅越重要）
        'comments': 1.5,   # 注释密度
    }
    
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
            "core_files": [],
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
            
            # 分析关键配置文件
            self._analyze_key_files(all_files, analysis_result)
            
            # 识别核心文件
            core_files = self._identify_core_files(all_files)
            analysis_result["core_files"] = [os.path.relpath(f, self.repo_path) for f in core_files]
            
            # 分析核心文件
            self._analyze_core_files(core_files, analysis_result)
            
            # 转换语言集合为列表
            analysis_result["languages"] = list(analysis_result["languages"])
            
            logger.info(f"代码仓库分析完成，识别到 {len(analysis_result['languages'])} 种语言，分析了 {len(analysis_result['files_analysis'])} 个文件")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"分析代码仓库失败: {str(e)}")
            raise
    
    def _analyze_key_files(self, all_files: List[str], analysis_result: Dict[str, Any]) -> None:
        """
        分析关键配置文件
        
        Args:
            all_files: 所有文件路径列表
            analysis_result: 分析结果字典
        """
        # 查找关键文件
        key_files = []
        for file_path in all_files:
            file_name = os.path.basename(file_path)
            if file_name in self.KEY_FILES:  # 注意这里不再包含README.md
                key_files.append(file_path)
        
        # 读取关键文件内容
        for file_path in key_files:
            rel_path = os.path.relpath(file_path, self.repo_path)
            file_content = FileHandler.read_file(file_path)
            
            # 添加到关键文件字典
            analysis_result["key_files"][rel_path] = file_content
    
    def _identify_core_files(self, all_files: List[str]) -> List[str]:
        """
        识别核心文件
        
        Args:
            all_files: 所有文件路径列表
            
        Returns:
            List[str]: 核心文件路径列表
        """
        logger.info("开始识别仓库核心文件")
        
        # 文件评分字典
        file_scores = {}
        
        # 统计文件被导入的次数
        import_counts = self._count_imports(all_files)
        
        # 分析每个文件
        for file_path in all_files:
            # 跳过自动生成的文件
            if self._is_generated_file(file_path):
                continue
                
            rel_path = os.path.relpath(file_path, self.repo_path)
            file_name = os.path.basename(file_path)
            
            # 跳过README文件
            if file_name.lower() == 'readme.md':
                continue
                
            # 初始化文件评分
            score = 0
            
            # 评分因素1: 文件大小(KB)
            try:
                size_kb = os.path.getsize(file_path) / 1024
                score += min(size_kb * self.WEIGHTS['size'], 10)  # 限制大小评分上限
            except:
                pass
                
            # 评分因素2: 文件路径深度
            depth = len(rel_path.split(os.sep))
            score += depth * self.WEIGHTS['depth']
            
            # 评分因素3: 被导入次数
            imports = import_counts.get(rel_path, 0)
            score += imports * self.WEIGHTS['imports']
            
            # 评分因素4: 注释密度
            comments_ratio = self._get_comments_ratio(file_path)
            score += comments_ratio * self.WEIGHTS['comments']
            
            # 评分因素5: 是否是入口文件
            if self._is_entry_point(file_path):
                score += 10
                
            # 记录文件评分
            file_scores[file_path] = score
        
        # 根据评分排序文件
        sorted_files = sorted(file_scores.items(), key=lambda x: x[1], reverse=True)
        
        # 选择评分最高的文件作为核心文件
        # 根据仓库大小动态调整核心文件数量
        core_files_count = min(max(5, len(all_files) // 10), 25)
        core_files = [file_path for file_path, _ in sorted_files[:core_files_count]]
        
        logger.info(f"已识别 {len(core_files)} 个核心文件")
        return core_files
    
    def _analyze_core_files(self, core_files: List[str], analysis_result: Dict[str, Any]) -> None:
        """
        分析核心文件
        
        Args:
            core_files: 核心文件路径列表
            analysis_result: 分析结果字典
        """
        for file_path in core_files:
            rel_path = os.path.relpath(file_path, self.repo_path)
            
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
                "size": len(file_content),
                "is_core": True
            }
    
    def _count_imports(self, all_files: List[str]) -> Dict[str, int]:
        """
        统计文件被导入的次数
        
        Args:
            all_files: 所有文件路径列表
            
        Returns:
            Dict[str, int]: 文件被导入次数的字典
        """
        import_counts = Counter()
        
        for file_path in all_files:
            content = FileHandler.read_file(file_path)
            if not content:
                continue
                
            # 获取文件语言
            language = CodeParser.identify_language(file_path)
            
            # 解析导入语句
            imported_files = CodeParser.parse_imports(content, language)
            
            # 将相对导入路径转换为绝对路径
            file_dir = os.path.dirname(file_path)
            for imp in imported_files:
                abs_path = os.path.normpath(os.path.join(file_dir, imp))
                if os.path.exists(abs_path):
                    rel_path = os.path.relpath(abs_path, self.repo_path)
                    import_counts[rel_path] += 1
                    
                # 处理没有扩展名的导入
                if os.path.splitext(abs_path)[1] == '':
                    for ext in ['.py', '.js', '.ts', '.jsx', '.tsx']:
                        path_with_ext = abs_path + ext
                        if os.path.exists(path_with_ext):
                            rel_path = os.path.relpath(path_with_ext, self.repo_path)
                            import_counts[rel_path] += 1
        
        return import_counts
    
    def _is_entry_point(self, file_path: str) -> bool:
        """
        判断文件是否可能是入口点
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否是入口点
        """
        file_name = os.path.basename(file_path)
        entry_patterns = [
            r'^main\.[^.]+$',
            r'^index\.[^.]+$',
            r'^app\.[^.]+$',
            r'^server\.[^.]+$',
            r'^cli\.[^.]+$'
        ]
        
        for pattern in entry_patterns:
            if re.match(pattern, file_name):
                return True
                
        # 检查文件内容中是否有main函数或类似入口点标志
        content = FileHandler.read_file(file_path)
        if content:
            language = CodeParser.identify_language(file_path)
            
            # Python入口点检查
            if language == 'Python' and ('if __name__ == "__main__"' in content or 'if __name__ == \'__main__\'' in content):
                return True
                
            # JavaScript/Node.js入口点检查
            if language in ['JavaScript', 'TypeScript'] and 'module.exports' in content:
                return True
                
        return False
    
    def _is_generated_file(self, file_path: str) -> bool:
        """
        判断文件是否是自动生成的
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否是自动生成的文件
        """
        file_name = os.path.basename(file_path)
        generated_patterns = [
            r'^.*\.min\.[^.]+$',  # 压缩文件
            r'^.*\.generated\.[^.]+$',  # 明确标记为生成的文件
            r'^.*\.d\.ts$',  # TypeScript声明文件
        ]
        
        for pattern in generated_patterns:
            if re.match(pattern, file_name):
                return True
                
        # 检查文件内容是否包含生成标记
        content = FileHandler.read_file(file_path)
        if content and content.strip():
            first_lines = '\n'.join(content.split('\n')[:5])
            generated_markers = [
                'Generated by', 'Auto-generated', 'DO NOT EDIT',
                'This file is generated', 'This is a generated file'
            ]
            
            for marker in generated_markers:
                if marker in first_lines:
                    return True
        
        return False
    
    def _get_comments_ratio(self, file_path: str) -> float:
        """
        获取文件的注释密度
        
        Args:
            file_path: 文件路径
            
        Returns:
            float: 注释密度（注释行数/总行数）
        """
        content = FileHandler.read_file(file_path)
        if not content:
            return 0
            
        language = CodeParser.identify_language(file_path)
        
        # 提取注释
        comments = CodeParser.extract_comments(content, language)
        
        # 计算注释密度
        total_lines = len(content.split('\n'))
        if total_lines == 0:
            return 0
            
        return len(comments) / total_lines
