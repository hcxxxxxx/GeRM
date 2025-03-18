import os
import logging
from typing import Dict, List, Set, Any

logger = logging.getLogger(__name__)

class CodeParser:
    """代码解析工具类"""
    
    # 支持的文件类型及其对应的语言
    SUPPORTED_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'React',
        '.tsx': 'React TypeScript',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.java': 'Java',
        '.kt': 'Kotlin',
        '.cpp': 'C++',
        '.c': 'C',
        '.h': 'C/C++ Header',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.m': 'Objective-C',
        '.cs': 'C#',
        '.sh': 'Shell',
        '.md': 'Markdown',
        '.json': 'JSON',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.xml': 'XML',
        '.sql': 'SQL',
    }
    
    # 需要忽略的目录
    IGNORED_DIRS = {
        'node_modules', 'venv', '.git', '.github', '__pycache__',
        'build', 'dist', '.idea', '.vscode', 'target', 'bin'
    }
    
    # 需要忽略的文件
    IGNORED_FILES = {
        '.DS_Store', '.gitignore', '.env', '.gitattributes'
    }
    
    @classmethod
    def identify_language(cls, file_path: str) -> str:
        """识别文件的编程语言"""
        _, ext = os.path.splitext(file_path)
        return cls.SUPPORTED_EXTENSIONS.get(ext.lower(), 'Unknown')
    
    @classmethod
    def should_ignore(cls, path: str) -> bool:
        """判断是否应该忽略该路径"""
        parts = path.split(os.sep)
        filename = os.path.basename(path)
        
        # 检查是否在忽略的目录中
        for part in parts:
            if part in cls.IGNORED_DIRS:
                return True
        
        # 检查是否是忽略的文件
        if filename in cls.IGNORED_FILES:
            return True
            
        return False
    
    @classmethod
    def parse_imports(cls, content: str, language: str) -> List[str]:
        """解析文件中的导入语句"""
        imports = []
        
        # 根据不同语言解析导入
        if language == 'Python':
            # 简单的Python导入解析
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    imports.append(line)
        
        # 可以添加其他语言的导入解析...
        
        return imports
    
    @classmethod
    def extract_comments(cls, content: str, language: str) -> List[str]:
        """提取文件中的注释"""
        comments = []
        
        # 根据不同语言提取注释
        if language == 'Python':
            # 简单的Python注释提取
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('#'):
                    comments.append(line)
        
        # 可以添加其他语言的注释提取...
        
        return comments
    
    @classmethod
    def identify_dependencies(cls, repo_path: str) -> Dict[str, Any]:
        """识别项目依赖"""
        dependencies = {}
        
        # 检查Python依赖
        req_files = ['requirements.txt', 'Pipfile', 'pyproject.toml']
        for req_file in req_files:
            req_path = os.path.join(repo_path, req_file)
            if os.path.exists(req_path):
                with open(req_path, 'r', encoding='utf-8') as f:
                    dependencies[req_file] = f.read()
        
        # 检查JavaScript依赖
        package_json = os.path.join(repo_path, 'package.json')
        if os.path.exists(package_json):
            try:
                import json
                with open(package_json, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                    if 'dependencies' in package_data:
                        dependencies['package.json:dependencies'] = package_data['dependencies']
                    if 'devDependencies' in package_data:
                        dependencies['package.json:devDependencies'] = package_data['devDependencies']
            except Exception as e:
                logger.error(f"解析package.json失败: {str(e)}")
        
        return dependencies
