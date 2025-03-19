import os
import uuid
import shutil
import tempfile
import logging
from flask import (
    render_template, request, redirect, url_for, flash, 
    current_app, jsonify, send_from_directory, abort
)
import markdown
from werkzeug.utils import secure_filename

from src.services.code_analyzer import CodeAnalyzer
from src.services.readme_generator import ReadmeGenerator
from web.forms import UploadRepoForm
from web.utils import extract_zip_file, clone_git_repo

logger = logging.getLogger(__name__)

def register_routes(app):
    """注册应用路由"""
    
    @app.route('/')
    def index():
        """渲染首页"""
        form = UploadRepoForm()
        return render_template('index.html', form=form)
    
    @app.route('/generate', methods=['POST'])
    def generate():
        """处理仓库上传并生成README"""
        form = UploadRepoForm()
        
        if not form.validate_on_submit():
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"错误: {getattr(form, field).label.text} - {error}", "danger")
            return redirect(url_for('index'))
        
        # 创建唯一ID用于本次生成
        generation_id = str(uuid.uuid4())
        
        try:
            # 创建临时目录
            temp_dir = tempfile.mkdtemp()
            
            # 上传方式：文件上传
            if form.repo_upload.data:
                zip_file = form.repo_upload.data
                zip_path = os.path.join(temp_dir, secure_filename(zip_file.filename))
                zip_file.save(zip_path)
                
                # 解压缩文件
                repo_dir = os.path.join(temp_dir, "repo")
                os.makedirs(repo_dir, exist_ok=True)
                extract_zip_file(zip_path, repo_dir)
                
            # 上传方式：Git URL
            elif form.repo_url.data:
                repo_url = form.repo_url.data
                repo_dir = os.path.join(temp_dir, "repo")
                clone_git_repo(repo_url, repo_dir)
            
            else:
                flash("请提供代码仓库（ZIP文件或Git URL）", "danger")
                return redirect(url_for('index'))
            
            # 检查是否成功提取/克隆仓库
            if not os.path.exists(repo_dir) or not os.listdir(repo_dir):
                flash("无法处理提供的仓库，请确保格式正确", "danger")
                return redirect(url_for('index'))
            
            # 创建输出目录
            output_dir = os.path.join(current_app.config["GENERATE_FOLDER"], generation_id)
            os.makedirs(output_dir, exist_ok=True)
            
            # 分析代码仓库
            code_analyzer = CodeAnalyzer(repo_dir)
            repo_analysis = code_analyzer.analyze()
            
            # 生成README内容
            readme_generator = ReadmeGenerator()
            readme_content = readme_generator.generate(repo_analysis)
            
            # 保存生成的README
            readme_path = os.path.join(output_dir, "README.md")
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(readme_content)
            
            # 保存仓库名称以便显示
            repo_name = repo_analysis.get("repo_name", "未知项目")
            repo_info_path = os.path.join(output_dir, "repo_info.txt")
            with open(repo_info_path, "w", encoding="utf-8") as f:
                f.write(repo_name)
            
            # 重定向到预览页面
            return redirect(url_for('preview', generation_id=generation_id))
            
        except Exception as e:
            logger.error(f"生成README时出错: {str(e)}", exc_info=True)
            flash(f"生成README时发生错误: {str(e)}", "danger")
            return redirect(url_for('index'))
        
        finally:
            # 清理临时目录
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                logger.warning(f"清理临时目录时出错: {str(e)}")
    
    @app.route('/preview/<generation_id>')
    def preview(generation_id):
        """预览生成的README"""
        # 检查生成ID是否存在
        generation_dir = os.path.join(current_app.config["GENERATE_FOLDER"], generation_id)
        if not os.path.exists(generation_dir):
            flash("找不到指定的生成结果", "danger")
            return redirect(url_for('index'))
        
        # 读取README内容
        readme_path = os.path.join(generation_dir, "README.md")
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                readme_content = f.read()
            
            # 转换Markdown为HTML
            readme_html = markdown.markdown(
                readme_content, 
                extensions=['tables', 'fenced_code', 'codehilite']
            )
            
            # 读取仓库名称
            repo_name = "未知项目"
            repo_info_path = os.path.join(generation_dir, "repo_info.txt")
            if os.path.exists(repo_info_path):
                with open(repo_info_path, "r", encoding="utf-8") as f:
                    repo_name = f.read().strip()
            
            return render_template(
                'preview.html', 
                generation_id=generation_id,
                repo_name=repo_name,
                readme_html=readme_html,
                readme_md=readme_content
            )
            
        except Exception as e:
            logger.error(f"预览README时出错: {str(e)}", exc_info=True)
            flash(f"预览README时发生错误: {str(e)}", "danger")
            return redirect(url_for('index'))
    
    @app.route('/download/<generation_id>')
    def download(generation_id):
        """下载生成的README文件"""
        generation_dir = os.path.join(current_app.config["GENERATE_FOLDER"], generation_id)
        if not os.path.exists(generation_dir):
            abort(404)
        
        return send_from_directory(
            generation_dir, 
            "README.md", 
            as_attachment=True,
            download_name="README.md"
        )
    
    @app.route('/about')
    def about():
        """关于页面"""
        return render_template('about.html')
    
    @app.errorhandler(404)
    def page_not_found(e):
        """404页面"""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        """500页面"""
        return render_template('500.html'), 500