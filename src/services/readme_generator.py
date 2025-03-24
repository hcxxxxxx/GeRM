import os
import logging
from typing import Dict, Any, List

from src.models.agent import ReadmeAgent

logger = logging.getLogger(__name__)

class ReadmeGenerator:
    """README生成服务类"""
    
    def __init__(self):
        """初始化GeRM"""
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
        
        # 优先处理核心文件
        core_files = processed.get("core_files", [])
        if core_files:
            logger.info(f"处理 {len(core_files)} 个核心文件")
            processed["core_files_info"] = self._process_core_files(core_files, processed.get("files_analysis", {}))
        
        # 提取所有文件的分析结果
        if "files_analysis" in processed:
            important_files = {}
            for path, analysis in processed["files_analysis"].items():
                # 包含更多有价值的信息
                file_info = {
                    "language": analysis.get("language", "Unknown"),
                    "summary": analysis.get("analysis", {}).get("purpose", ""),
                    "is_core": analysis.get("is_core", False)
                }
                
                # 如果有组件信息，也包含进来
                if "analysis" in analysis and "components" in analysis["analysis"]:
                    file_info["components"] = analysis["analysis"]["components"]
                
                # 如果有依赖信息，也包含进来
                if "analysis" in analysis and "dependencies" in analysis["analysis"]:
                    file_info["dependencies"] = analysis["analysis"]["dependencies"]
                
                important_files[path] = file_info
            
            processed["important_files"] = important_files
        
        # 构建项目架构概述
        processed["architecture_summary"] = self._build_architecture_summary(processed)
        
        # 确保依赖格式一致并提取关键依赖
        if "dependencies" in processed:
            processed["key_dependencies"] = self._extract_key_dependencies(processed["dependencies"])
        
        # 添加仓库名称和路径
        if "repo_name" not in processed:
            processed["repo_name"] = "Unknown Project"
        
        return processed
    
    def _process_core_files(self, core_files: List[str], files_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理核心文件信息
        
        Args:
            core_files: 核心文件列表
            files_analysis: 文件分析结果
            
        Returns:
            Dict[str, Any]: 处理后的核心文件信息
        """
        core_files_info = {}
        
        # 按照目录分组核心文件
        files_by_dir = {}
        for file_path in core_files:
            dir_name = os.path.dirname(file_path) or "root"
            if dir_name not in files_by_dir:
                files_by_dir[dir_name] = []
            files_by_dir[dir_name].append(file_path)
        
        # 处理每个目录的核心文件
        for dir_name, dir_files in files_by_dir.items():
            dir_info = {
                "files": [],
                "purpose": self._infer_directory_purpose(dir_name, dir_files, files_analysis)
            }
            
            # 处理目录中的每个文件
            for file_path in dir_files:
                if file_path in files_analysis:
                    analysis = files_analysis[file_path]
                    file_info = {
                        "name": os.path.basename(file_path),
                        "path": file_path,
                        "language": analysis.get("language", "Unknown"),
                        "purpose": analysis.get("analysis", {}).get("purpose", "")
                    }
                    dir_info["files"].append(file_info)
            
            core_files_info[dir_name] = dir_info
        
        return core_files_info
    
    def _infer_directory_purpose(self, dir_name: str, files: List[str], files_analysis: Dict[str, Any]) -> str:
        """
        推断目录的用途
        
        Args:
            dir_name: 目录名称
            files: 目录中的文件列表
            files_analysis: 文件分析结果
            
        Returns:
            str: 目录用途描述
        """
        # 基于目录名称的常见模式
        common_dirs = {
            "src": "源代码目录",
            "lib": "库文件目录",
            "utils": "实用工具目录",
            "helpers": "辅助函数目录",
            "components": "组件目录",
            "models": "数据模型目录", 
            "controllers": "控制器目录",
            "views": "视图目录",
            "services": "服务目录",
            "api": "API相关代码目录",
            "tests": "测试目录",
            "docs": "文档目录",
            "config": "配置目录",
            "scripts": "脚本目录",
            "static": "静态资源目录",
            "public": "公共资源目录",
            "assets": "资源文件目录",
            "root": "项目根目录"
        }
        
        # 从目录名推断用途
        base_dir = os.path.basename(dir_name)
        if base_dir in common_dirs:
            return common_dirs[base_dir]
        
        # 尝试从文件分析中推断目录用途
        purposes = []
        for file_path in files:
            if file_path in files_analysis and "analysis" in files_analysis[file_path]:
                purpose = files_analysis[file_path]["analysis"].get("purpose", "")
                if purpose:
                    purposes.append(purpose)
        
        # 如果有足够的文件用途描述，组合它们
        if purposes:
            common_words = self._extract_common_themes(purposes)
            if common_words:
                return f"{base_dir}目录: {common_words}"
        
        return f"{base_dir}目录"
    
    def _extract_common_themes(self, texts: List[str]) -> str:
        """
        从一组文本中提取共同主题
        
        Args:
            texts: 文本列表
            
        Returns:
            str: 共同主题描述
        """
        # 这个实现非常简化，实际中可能需要更复杂的NLP方法
        if not texts:
            return ""
            
        # 简单返回第一个非空描述
        for text in texts:
            if text and len(text) > 10:  # 确保描述有一定长度
                return text[:100] + "..." if len(text) > 100 else text
                
        return ""
    
    def _build_architecture_summary(self, analysis: Dict[str, Any]) -> str:
        """
        构建项目架构概述
        
        Args:
            analysis: 分析结果
            
        Returns:
            str: 架构概述
        """
        repo_name = analysis.get("repo_name", "Unknown Project")
        languages = analysis.get("languages", [])
        
        summary = f"{repo_name}是一个"
        
        # 添加语言信息
        if languages:
            if len(languages) == 1:
                summary += f"使用{languages[0]}开发的"
            else:
                lang_str = "、".join(languages[:-1]) + "和" + languages[-1]
                summary += f"使用{lang_str}开发的"
        
        # 尝试从分析结果中找出项目类型
        project_type = self._infer_project_type(analysis)
        if project_type:
            summary += f"{project_type}。"
        else:
            summary += "项目。"
        
        # 添加目录结构概述
        if "core_files_info" in analysis:
            summary += "项目的主要模块包括："
            modules = []
            for dir_name, dir_info in analysis["core_files_info"].items():
                if dir_name != "root" and dir_info["purpose"]:
                    modules.append(dir_info["purpose"])
            
            if modules:
                summary += "、".join(modules) + "。"
        
        return summary
    
    def _infer_project_type(self, analysis: Dict[str, Any]) -> str:
        """
        推断项目类型
        
        Args:
            analysis: 分析结果
            
        Returns:
            str: 项目类型描述
        """
        # 从依赖和文件结构推断项目类型
        dependencies = analysis.get("dependencies", {})
        
        # 推断Web应用
        web_frameworks = ["flask", "django", "fastapi", "express", "react", "vue", "angular"]
        for dep in dependencies.values():
            if isinstance(dep, str):
                for framework in web_frameworks:
                    if framework in dep.lower():
                        return "Web应用"
        
        # 推断CLI工具
        if "click" in str(dependencies) or "argparse" in str(dependencies) or "commander" in str(dependencies):
            return "命令行工具"
        
        # 推断数据科学项目
        data_libs = ["pandas", "numpy", "scikit-learn", "tensorflow", "pytorch"]
        for dep in dependencies.values():
            if isinstance(dep, str):
                for lib in data_libs:
                    if lib in dep.lower():
                        return "数据科学项目"
        
        # 默认返回空
        return ""
    
    def _extract_key_dependencies(self, dependencies: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取关键依赖
        
        Args:
            dependencies: 依赖信息
            
        Returns:
            Dict[str, Any]: 关键依赖信息
        """
        key_deps = {}
        
        for file, deps in dependencies.items():
            if isinstance(deps, dict):
                # 对于package.json类型的依赖
                key_deps[file] = deps
            elif isinstance(deps, str):
                # 对于requirements.txt类型的依赖，只保留非空行
                lines = [line.strip() for line in deps.split('\n') if line.strip() and not line.startswith('#')]
                key_deps[file] = lines
        
        return key_deps
