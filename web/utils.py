import os
import zipfile
import subprocess
import logging
import shutil
from typing import Optional

logger = logging.getLogger(__name__)

def extract_zip_file(zip_path: str, output_dir: str) -> bool:
    """
    解压ZIP文件到指定目录
    
    Args:
        zip_path: ZIP文件路径
        output_dir: 输出目录
        
    Returns:
        bool: 是否成功解压
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        
        # 检查是否解压出单个目录
        contents = os.listdir(output_dir)
        if len(contents) == 1 and os.path.isdir(os.path.join(output_dir, contents[0])):
            # 如果是单个目录，将其内容移动到输出目录
            inner_dir = os.path.join(output_dir, contents[0])
            for item in os.listdir(inner_dir):
                shutil.move(
                    os.path.join(inner_dir, item),
                    os.path.join(output_dir, item)
                )
            os.rmdir(inner_dir)
        
        return True
    except Exception as e:
        logger.error(f"解压ZIP文件失败: {str(e)}")
        return False

def clone_git_repo(repo_url: str, output_dir: str) -> bool:
    """
    克隆Git仓库到指定目录
    
    Args:
        repo_url: Git仓库URL
        output_dir: 输出目录
        
    Returns:
        bool: 是否成功克隆
    """
    try:
        # 执行git clone命令
        subprocess.run(
            ["git", "clone", "--depth=1", repo_url, output_dir],
            check=True,
            capture_output=True
        )
        
        # 删除.git目录以减小大小
        git_dir = os.path.join(output_dir, ".git")
        if os.path.exists(git_dir):
            shutil.rmtree(git_dir)
        
        return True
    except Exception as e:
        logger.error(f"克隆Git仓库失败: {str(e)}")
        return False

def sanitize_filename(filename: str) -> str:
    """
    清理文件名，确保安全
    
    Args:
        filename: 原始文件名
        
    Returns:
        str: 清理后的文件名
    """
    # 替换不安全字符
    for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
        filename = filename.replace(char, '_')
    
    return filename

def get_file_size_mb(file_path: str) -> float:
    """
    获取文件大小（MB）
    
    Args:
        file_path: 文件路径
        
    Returns:
        float: 文件大小（MB）
    """
    return os.path.getsize(file_path) / (1024 * 1024)