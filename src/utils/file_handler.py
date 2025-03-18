import os
import logging
from typing import Dict, List, Set, Any, Optional

logger = logging.getLogger(__name__)

class FileHandler:
    """文件处理工具类"""
    
    @staticmethod
    def read_file(file_path: str, encoding: str = 'utf-8') -> str:
        """
        读取文件内容
        
        Args:
            file_path: 文件路径
            encoding: 文件编码，默认utf-8
            
        Returns:
            str: 文件内容
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content
        except UnicodeDecodeError:
            # 如果UTF-8解码失败，尝试其他编码
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                return content
            except Exception as e:
                logger.warning(f"无法读取文件 {file_path}: {str(e)}")
                return f"[无法读取文件内容: {str(e)}]"
        except Exception as e:
            logger.warning(f"读取文件 {file_path} 失败: {str(e)}")
            return f"[读取文件失败: {str(e)}]"
    
    @staticmethod
    def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """
        写入文件内容
        
        Args:
            file_path: 文件路径
            content: 要写入的内容
            encoding: 文件编码，默认utf-8
            
        Returns:
            bool: 是否成功写入
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"写入文件 {file_path} 失败: {str(e)}")
            return False
    
    @staticmethod
    def list_files(dir_path: str, ignore_func: Optional[callable] = None) -> List[str]:
        """
        列出目录中的所有文件
        
        Args:
            dir_path: 目录路径
            ignore_func: 用于判断是否忽略文件的函数
            
        Returns:
            List[str]: 文件路径列表
        """
        file_list = []
        
        try:
            for root, dirs, files in os.walk(dir_path):
                # 如果提供了忽略函数，过滤目录
                if ignore_func:
                    dirs[:] = [d for d in dirs if not ignore_func(os.path.join(root, d))]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # 如果提供了忽略函数，过滤文件
                    if ignore_func and ignore_func(file_path):
                        continue
                        
                    file_list.append(file_path)
                    
            return file_list
            
        except Exception as e:
            logger.error(f"列出目录 {dir_path} 中的文件失败: {str(e)}")
            return []
    
    @staticmethod
    def get_repo_structure(repo_path: str, ignore_func: Optional[callable] = None) -> Dict[str, Any]:
        """
        获取代码仓库结构
        
        Args:
            repo_path: 仓库路径
            ignore_func: 用于判断是否忽略文件的函数
            
        Returns:
            Dict[str, Any]: 仓库结构
        """
        try:
            structure = {"name": os.path.basename(repo_path), "type": "directory", "children": []}
            
            def build_structure(path, parent):
                """递归构建目录结构"""
                try:
                    items = os.listdir(path)
                    for item in sorted(items):
                        item_path = os.path.join(path, item)
                        
                        # 如果提供了忽略函数，过滤文件和目录
                        if ignore_func and ignore_func(item_path):
                            continue
                            
                        if os.path.isdir(item_path):
                            # 目录
                            dir_node = {"name": item, "type": "directory", "children": []}
                            parent["children"].append(dir_node)
                            build_structure(item_path, dir_node)
                        else:
                            # 文件
                            parent["children"].append({"name": item, "type": "file"})
                except Exception as e:
                    logger.warning(f"构建 {path} 的结构失败: {str(e)}")
            
            build_structure(repo_path, structure)
            return structure
            
        except Exception as e:
            logger.error(f"获取仓库 {repo_path} 结构失败: {str(e)}")
            return {"name": os.path.basename(repo_path), "type": "directory", "children": [], "error": str(e)}
