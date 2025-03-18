import json
from typing import Dict, Any, List

class PromptTemplates:
    """提示词模板类"""

    @staticmethod
    def get_readme_generation_prompt(repo_analysis: Dict[str, Any]) -> str:
        """
        获取README生成提示词
        
        Args:
            repo_analysis: 仓库分析结果
            
        Returns:
            str: 格式化的提示词
        """
        # 将仓库分析结果转换为JSON字符串
        repo_json = json.dumps(repo_analysis, indent=2, ensure_ascii=False)
        
        # 构建提示词
        prompt = f"""请根据以下代码仓库的分析结果，生成一个专业的README.md文件。

        仓库分析结果:
        ```json
        {repo_json}
        ```
        
        生成README时，请考虑以下要点:
        - 开始用一个简短清晰的项目描述
        - 列出主要特性和功能
        - 包含安装说明
        - 提供使用示例和API文档（如果适用）
        - 解释项目架构和主要组件
        - 包含技术栈信息
        - 添加贡献指南（如果适用）
        - 添加许可证信息（如果找到）
        - 使用Markdown格式，包括标题、列表、代码块等
        - 确保README清晰、专业、易于阅读

        请直接生成完整的README.md内容，使用Markdown格式，不需要额外的解释。
        """
        return prompt

    @staticmethod
    def get_file_analysis_prompt(file_path: str, file_content: str) -> str:
        """
        获取文件分析提示词
        
        Args:
            file_path: 文件路径
            file_content: 文件内容
            
        Returns:
            str: 格式化的提示词
        """
        # 构建文件分析提示词
        prompt = f"""请分析以下代码文件，提取关键信息并以JSON格式返回结果：
        
        文件路径: {file_path}
        
        文件内容:
        ```
        {file_content[:10000]}  # 限制内容长度
        {"..." if len(file_content) > 10000 else ""}
        ```

        请提取以下信息并以JSON格式返回：
        - 文件的主要目的和功能
        - 主要类、函数或组件
        - 依赖关系
        - 核心逻辑
        - 配置信息（如果有）
        - 代码质量评估
        
        JSON格式示例:
        ```json
        {{
            "purpose": "文件的主要目的",
            "components": ["主要类或函数1", "主要类或函数2"],
            "dependencies": ["依赖1", "依赖2"],
            "logic": "核心逻辑概述",
            "configuration": "配置信息",
            "quality": "代码质量评估"
        }}
        ```

        请确保返回有效的JSON格式。
        """
        return prompt

    @staticmethod
    def get_repo_summary_prompt(repo_structure: Dict[str, Any], key_files_content: Dict[str, str]) -> str:
        """
        获取仓库摘要提示词
        
        Args:
            repo_structure: 仓库结构
            key_files_content: 关键文件内容
            
        Returns:
            str: 格式化的提示词
        """
        # 将仓库结构转换为JSON字符串
        structure_json = json.dumps(repo_structure, indent=2, ensure_ascii=False)
        
        # 构建关键文件内容字符串
        key_files_str = ""
        for file_path, content in key_files_content.items():
            key_files_str += f"\n--- {file_path} ---\n"
            key_files_str += content[:1000]  # 限制每个文件内容长度
            if len(content) > 1000:
                key_files_str += "\n...(内容已截断)...\n"
        
        # 构建提示词
        prompt = f"""请分析以下代码仓库的结构和关键文件内容，提供一个全面的项目摘要。

        仓库结构:
        ```json
        {structure_json}
        ```

        关键文件内容:
        {key_files_str}

        请提供以下内容:
        - 项目的主要用途和功能
        - 技术栈和主要依赖
        - 项目架构概述
        - 主要组件和它们的功能
        - 推荐的安装和使用步骤
        - 项目的亮点和特色

        请以JSON格式返回分析结果，确保返回有效的JSON。
        """
        return prompt
