/**
 * 对话逻辑模块
 * 处理用户输入、发送消息、显示响应
 */

// 对话状态
let sessionId = null;
let isProcessing = false;

/**
 * 初始化对话
 */
function initChat() {
    // 生成会话 ID
    sessionId = `session_${Date.now()}`;
    
    // 绑定事件
    bindEvents();
    
    // 显示欢迎消息
    showWelcomeMessage();
}

/**
 * 绑定事件
 */
function bindEvents() {
    const input = document.getElementById('user-input');
    const btnSend = document.getElementById('btn-send');
    const btnClear = document.getElementById('btn-clear');
    
    // 发送按钮点击事件
    btnSend.addEventListener('click', () => sendMessage());
    
    // 输入框回车事件
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // 清空按钮点击事件
    btnClear.addEventListener('click', clearChat);
    
    // 快速输入按钮
    document.querySelectorAll('.hint-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            input.value = btn.dataset.text;
            input.focus();
        });
    });
}

/**
 * 发送消息
 */
async function sendMessage() {
    if (isProcessing) {
        return;
    }
    
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) {
        return;
    }
    
    // 显示用户消息
    appendMessage('user', message);
    
    // 清空输入框
    input.value = '';
    
    // 设置处理状态
    isProcessing = true;
    utils.setLoading(document.getElementById('btn-send'), true);
    
    // 显示加载状态
    appendLoadingMessage();
    
    try {
        // 1. 调用科室推荐 API
        const deptResult = await api.recommendDepartment(message);
        
        // 2. 显示科室推荐结果
        components.renderDepartmentCards(deptResult.departments);
        components.showResultCard('department-result');
        
        // 3. 获取第一个推荐科室，查询医生和费用
        if (deptResult.departments && deptResult.departments.length > 0) {
            const topDept = deptResult.departments[0].name;
            
            // 并行调用医生和费用 API
            const [doctorResult, costResult] = await Promise.all([
                api.searchDoctors(topDept),
                api.estimateCost(topDept),
            ]);
            
            // 显示医生推荐
            if (doctorResult.doctors && doctorResult.doctors.length > 0) {
                components.renderDoctorCards(doctorResult.doctors);
                components.showResultCard('doctor-result');
            }
            
            // 显示费用估算
            components.renderCostDetail(costResult);
            components.showResultCard('cost-result');
        }
        
        // 4. 显示 AI 回复消息
        removeLoadingMessage();
        const replyText = generateReplyText(deptResult);
        appendMessage('assistant', replyText);
        
    } catch (error) {
        console.error('Send Message Error:', error);
        removeLoadingMessage();
        appendMessage('assistant', `抱歉，处理您的请求时出现错误：${error.message}`);
    } finally {
        isProcessing = false;
        utils.setLoading(document.getElementById('btn-send'), false);
    }
}

/**
 * 生成回复文本
 */
function generateReplyText(deptResult) {
    let text = deptResult.reason + '\n\n';
    
    if (deptResult.departments && deptResult.departments.length > 0) {
        text += '推荐科室：\n';
        deptResult.departments.forEach((dept, index) => {
            text += `${index + 1}. ${dept.name} (置信度 ${(dept.confidence * 100).toFixed(0)}%)\n`;
            text += `   ${dept.reason}\n`;
        });
        
        text += '\n我已为您查询了该科室的医生和预估费用，请查看右侧详情。';
    }
    
    return text;
}

/**
 * 显示欢迎消息
 */
function showWelcomeMessage() {
    // 已经在 HTML 中静态定义了欢迎消息
}

/**
 * 添加消息到对话列表
 */
function appendMessage(role, text) {
    const messageList = document.getElementById('message-list');
    
    const messageDiv = utils.createElement('div', {
        className: `message ${role}`,
    }, [
        utils.createElement('div', { className: 'message-avatar' }, [
            role === 'user' ? '👤' : '🤖',
        ]),
        utils.createElement('div', { className: 'message-content' }, [
            utils.createElement('div', { className: 'message-text', textContent: text }),
        ]),
    ]);
    
    messageList.appendChild(messageDiv);
    utils.scrollToBottom(messageList);
}

/**
 * 添加加载状态消息
 */
function appendLoadingMessage() {
    const messageList = document.getElementById('message-list');
    
    const loadingDiv = utils.createElement('div', {
        className: 'message assistant',
        id: 'loading-message',
    }, [
        utils.createElement('div', { className: 'message-avatar' }, ['🤖']),
        utils.createElement('div', { className: 'message-content' }, [
            utils.createElement('div', { className: 'loading-dots' }, [
                utils.createElement('span'),
                utils.createElement('span'),
                utils.createElement('span'),
            ]),
        ]),
    ]);
    
    messageList.appendChild(loadingDiv);
    utils.scrollToBottom(messageList);
}

/**
 * 移除加载状态消息
 */
function removeLoadingMessage() {
    const loadingMessage = document.getElementById('loading-message');
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

/**
 * 清空对话
 */
function clearChat() {
    const messageList = document.getElementById('message-list');
    
    // 保留第一条欢迎消息
    const welcomeMessage = messageList.querySelector('.message');
    messageList.innerHTML = '';
    if (welcomeMessage) {
        messageList.appendChild(welcomeMessage);
    }
    
    // 隐藏结果卡片
    components.hideResultCard('department-result');
    components.hideResultCard('doctor-result');
    components.hideResultCard('cost-result');
    
    // 重新生成会话 ID
    sessionId = `session_${Date.now()}`;
}

/**
 * 初始化
 */
document.addEventListener('DOMContentLoaded', initChat);
