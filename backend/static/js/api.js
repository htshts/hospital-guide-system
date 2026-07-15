/**
 * API 请求封装模块
 * 处理所有与后端 API 的通信
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * 通用 API 请求函数
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const finalOptions = {
        ...defaultOptions,
        ...options,
    };
    
    try {
        const response = await fetch(url, finalOptions);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

/**
 * 科室推荐 API
 */
async function recommendDepartment(symptoms) {
    return await apiRequest('/api/v1/department/recommend', {
        method: 'POST',
        body: JSON.stringify({ symptoms }),
    });
}

/**
 * 医生查询 API
 */
async function searchDoctors(department, scheduleDay = null) {
    const params = new URLSearchParams();
    params.append('department', department);
    if (scheduleDay) {
        params.append('schedule_day', scheduleDay);
    }
    
    return await apiRequest(`/api/v1/doctors?${params.toString()}`);
}

/**
 * 费用估算 API
 */
async function estimateCost(department, procedures = null) {
    const body = { department };
    if (procedures) {
        body.procedures = procedures;
    }
    
    return await apiRequest('/api/v1/cost/estimate', {
        method: 'POST',
        body: JSON.stringify(body),
    });
}

/**
 * 发送聊天消息 API
 */
async function sendChatMessage(sessionId, message) {
    return await apiRequest('/api/v1/chat/send', {
        method: 'POST',
        body: JSON.stringify({
            session_id: sessionId,
            message,
        }),
    });
}

// 导出函数
window.api = {
    recommendDepartment,
    searchDoctors,
    estimateCost,
    sendChatMessage,
};
