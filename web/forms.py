from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import Optional, URL, ValidationError

class UploadRepoForm(FlaskForm):
    """代码仓库上传表单"""
    
    repo_upload = FileField(
        '上传ZIP文件',
        validators=[
            FileAllowed(['zip'], '只允许上传ZIP文件')
        ]
    )
    
    repo_url = StringField(
        'Git仓库URL',
        validators=[
            Optional(),
            URL(message='请输入有效的URL')
        ]
    )
    
    submit = SubmitField('生成README')
    
    def validate(self):
        """确保至少提供一种仓库上传方式"""
        if not super().validate():
            return False
        
        if not self.repo_upload.data and not self.repo_url.data:
            self.repo_upload.errors.append('请上传ZIP文件或提供Git仓库URL')
            return False
        
        return True