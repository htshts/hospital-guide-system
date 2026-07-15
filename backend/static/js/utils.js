/**
 * 工具函数模块
 */

/**
 * 格式化时间
 */
function formatTime(date = new Date()) {
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

/**
 * 防抖函数
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * 节流函数
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * 显示/隐藏加载状态
 */
function setLoading(element, isLoading) {
    if (isLoading) {
        element.disabled = true;
        element.querySelector('.btn-text').style.display = 'none';
        element.querySelector('.btn-loading').style.display = 'inline';
    } else {
        element.disabled = false;
        element.querySelector('.btn-text').style.display = 'inline';
        element.querySelector('.btn-loading').style.display = 'none';
    }
}

/**
 * 滚动到元素底部
 */
function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight;
}

/**
 * 创建 DOM 元素
 */
function createElement(tag, attributes = {}, children = []) {
    const element = document.createElement(tag);
    
    // 设置属性
    for (const [key, value] of Object.entries(attributes)) {
        if (key === 'className') {
            element.className = value;
        } else if (key === 'textContent') {
            element.textContent = value;
        } else if (key === 'innerHTML') {
            element.innerHTML = value;
        } else if (key.startsWith('on')) {
            const event = key.toLowerCase().slice(2);
            element.addEventListener(event, value);
        } else {
            element.setAttribute(key, value);
        }
    }
    
    // 添加子元素
    if (Array.isArray(children)) {
        children.forEach(child => {
            if (typeof child === 'string') {
                element.appendChild(document.createTextNode(child));
            } else if (child instanceof HTMLElement) {
                element.appendChild(child);
            }
        });
    } else if (typeof children === 'string') {
        element.textContent = children;
    }
    
    return element;
}

// 导出函数
window.utils = {
    formatTime,
    debounce,
    throttle,
    setLoading,
    scrollToBottom,
    createElement,
};
