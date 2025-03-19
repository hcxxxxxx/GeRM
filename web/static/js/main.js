// 主JavaScript文件

// 处理闪现消息关闭
document.addEventListener('DOMContentLoaded', function() {
    const closeButtons = document.querySelectorAll('.flash-message .close-btn');
    
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.parentElement;
            
            // 添加淡出动画
            message.style.opacity = '0';
            message.style.transform = 'translateY(-10px)';
            message.style.transition = 'opacity 0.3s, transform 0.3s';
            
            // 动画完成后移除元素
            setTimeout(() => {
                message.remove();
            }, 300);
        });
    });
    
    // 自动隐藏闪现消息
    const flashMessages = document.querySelectorAll('.flash-message');
    
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(message => {
                // 添加淡出动画
                message.style.opacity = '0';
                message.style.transform = 'translateY(-10px)';
                message.style.transition = 'opacity 0.3s, transform 0.3s';
                
                // 动画完成后移除元素
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }, 5000); // 5秒后自动隐藏
    }
});

// 添加科技感动画效果
document.addEventListener('DOMContentLoaded', function() {
    // 为代码编辑器添加打字机效果
    const codeContent = document.querySelector('.code-content code');
    
    if (codeContent) {
        const originalText = codeContent.textContent;
        codeContent.textContent = '';
        
        let i = 0;
        const typeText = () => {
            if (i < originalText.length) {
                codeContent.textContent += originalText.charAt(i);
                i++;
                setTimeout(typeText, Math.random() * 50 + 10);
            }
        };
        
        // 延迟开始打字效果
        setTimeout(typeText, 500);
    }
    
    // 为卡片添加进入动画
    const animateItems = document.querySelectorAll('.card, .feature-card');
    
    if (animateItems.length > 0) {
        // 检查元素是否在视口内
        const isInViewport = (element) => {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        };
        
        // 设置初始状态
        animateItems.forEach(item => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            item.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        });
        
        // 动画函数
        const animateOnScroll = () => {
            animateItems.forEach(item => {
                if (isInViewport(item) && item.style.opacity === '0') {
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'translateY(0)';
                    }, 100);
                }
            });
        };
        
        // 初始检查
        animateOnScroll();
        
        // 滚动时检查
        window.addEventListener('scroll', animateOnScroll);
    }
});