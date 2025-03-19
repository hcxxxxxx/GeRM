// 预览功能JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 代码高亮
    if (document.querySelector('#markdown code')) {
        // 添加行号
        const codeBlocks = document.querySelectorAll('#markdown pre code');
        codeBlocks.forEach(block => {
            const lines = block.textContent.split('\n');
            let numberedLines = '';
            
            lines.forEach((line, index) => {
                if (index === lines.length - 1 && line === '') return;
                numberedLines += `<span class="line-number">${index + 1}</span>${line}\n`;
            });
            
            // 使用innerHTML安全，因为这是我们控制的内容
            block.innerHTML = numberedLines;
        });
    }
    
    // 添加滚动同步
    const previewPane = document.getElementById('preview');
    const markdownPane = document.getElementById('markdown');
    
    if (previewPane && markdownPane) {
        // 从预览滚动到Markdown
        previewPane.addEventListener('scroll', function() {
            const previewScrollPercentage = previewPane.scrollTop / (previewPane.scrollHeight - previewPane.clientHeight);
            markdownPane.scrollTop = previewScrollPercentage * (markdownPane.scrollHeight - markdownPane.clientHeight);
        });
        
        // 从Markdown滚动到预览
        markdownPane.addEventListener('scroll', function() {
            const markdownScrollPercentage = markdownPane.scrollTop / (markdownPane.scrollHeight - markdownPane.clientHeight);
            previewPane.scrollTop = markdownScrollPercentage * (previewPane.scrollHeight - previewPane.clientHeight);
        });
    }
    
    // 添加锚点链接功能
    const headings = document.querySelectorAll('.markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4, .markdown-body h5, .markdown-body h6');
    
    headings.forEach(heading => {
        // 创建ID
        const id = heading.textContent
            .toLowerCase()
            .replace(/[^\w\s-]/g, '')
            .replace(/[\s_-]+/g, '-')
            .replace(/^-+|-+$/g, '');
            
        heading.id = id;
        
        // 添加锚点链接
        const anchor = document.createElement('a');
        anchor.className = 'heading-anchor';
        anchor.href = `#${id}`;
        anchor.innerHTML = ' 🔗';
        anchor.style.opacity = '0';
        anchor.style.textDecoration = 'none';
        anchor.style.transition = 'opacity 0.2s';
        
        heading.appendChild(anchor);
        
        // 鼠标悬停时显示锚点
        heading.addEventListener('mouseenter', () => {
            anchor.style.opacity = '0.5';
        });
        
        heading.addEventListener('mouseleave', () => {
            anchor.style.opacity = '0';
        });
    });
});