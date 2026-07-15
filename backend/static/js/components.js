/**
 * UI 组件模块
 * 负责渲染各种卡片和界面元素
 */

/**
 * 渲染科室推荐卡片
 */
function renderDepartmentCards(departments) {
    const container = document.getElementById('department-list');
    container.innerHTML = '';
    
    departments.forEach(dept => {
        const card = utils.createElement('div', {
            className: 'department-card',
        }, [
            utils.createElement('div', { className: 'department-name' }, [
                utils.createElement('span', { textContent: dept.name }),
                utils.createElement('span', {
                    textContent: `${(dept.confidence * 100).toFixed(0)}%`,
                    style: 'font-size: 14px; color: #1890ff;',
                }),
            ]),
            utils.createElement('div', { className: 'confidence-bar' }, [
                utils.createElement('div', {
                    className: 'confidence-fill',
                    style: `width: ${dept.confidence * 100}%`,
                }),
            ]),
            utils.createElement('div', {
                className: 'department-reason',
                textContent: dept.reason,
            }),
        ]);
        
        container.appendChild(card);
    });
}

/**
 * 渲染医生推荐卡片
 */
function renderDoctorCards(doctors) {
    const container = document.getElementById('doctor-list');
    container.innerHTML = '';
    
    doctors.forEach(doctor => {
        const card = utils.createElement('div', {
            className: 'doctor-card',
        }, [
            utils.createElement('div', { className: 'doctor-header' }, [
                utils.createElement('div', { className: 'doctor-name', textContent: doctor.name }),
                utils.createElement('span', { className: 'doctor-title', textContent: doctor.title }),
            ]),
            utils.createElement('div', { className: 'doctor-info', textContent: `科室：${doctor.department}` }),
            utils.createElement('div', { className: 'doctor-info', textContent: `专长：${doctor.specialty}` }),
            utils.createElement('div', { className: 'doctor-info', textContent: `评分：${'⭐'.repeat(Math.floor(doctor.rating))} (${doctor.rating})` }),
            utils.createElement('div', { className: 'doctor-info', textContent: `从业：${doctor.experience_years}年` }),
        ]);
        
        // 添加排班信息
        if (doctor.schedule) {
            const scheduleContainer = utils.createElement('div', { className: 'doctor-schedule' });
            
            for (const [day, time] of Object.entries(doctor.schedule)) {
                const tag = utils.createElement('span', {
                    className: `schedule-tag ${time !== '休息' ? 'available' : ''}`,
                    textContent: `${day}: ${time}`,
                });
                scheduleContainer.appendChild(tag);
            }
            
            card.appendChild(scheduleContainer);
        }
        
        container.appendChild(card);
    });
}

/**
 * 渲染费用估算卡片
 */
function renderCostDetail(costData) {
    const container = document.getElementById('cost-detail');
    container.innerHTML = '';
    
    // 费用汇总
    const summary = utils.createElement('div', { className: 'cost-summary' }, [
        utils.createElement('div', { className: 'cost-item' }, [
            utils.createElement('div', { className: 'cost-label', textContent: '总费用' }),
            utils.createElement('div', { className: 'cost-value total', textContent: `¥${costData.total}` }),
        ]),
        utils.createElement('div', { className: 'cost-item' }, [
            utils.createElement('div', { className: 'cost-label', textContent: '医保支付' }),
            utils.createElement('div', { className: 'cost-value insurance', textContent: `¥${costData.insurance_pay}` }),
        ]),
        utils.createElement('div', { className: 'cost-item' }, [
            utils.createElement('div', { className: 'cost-label', textContent: '自费金额' }),
            utils.createElement('div', { className: 'cost-value self-pay', textContent: `¥${costData.self_pay}` }),
        ]),
    ]);
    
    container.appendChild(summary);
    
    // 费用明细
    if (costData.breakdown && costData.breakdown.length > 0) {
        const breakdownTitle = utils.createElement('div', {
            className: 'cost-breakdown-title',
            textContent: '费用明细：',
            style: 'font-weight: 600; margin-top: 16px; margin-bottom: 8px;',
        });
        container.appendChild(breakdownTitle);
        
        const breakdownList = utils.createElement('div', { className: 'cost-breakdown' });
        
        costData.breakdown.forEach(item => {
            const row = utils.createElement('div', { className: 'breakdown-item' }, [
                utils.createElement('span', { textContent: item.name }),
                utils.createElement('span', { textContent: `¥${item.price} (医保${item.insurance_rate * 100}%)` }),
            ]);
            breakdownList.appendChild(row);
        });
        
        container.appendChild(breakdownList);
    }
    
    // 医保政策
    if (costData.insurance_policy) {
        const policy = utils.createElement('div', {
            className: 'insurance-policy',
            textContent: costData.insurance_policy,
        });
        container.appendChild(policy);
    }
}

/**
 * 显示/隐藏结果卡片
 */
function showResultCard(cardId) {
    document.getElementById(cardId).style.display = 'block';
}

function hideResultCard(cardId) {
    document.getElementById(cardId).style.display = 'none';
}

// 导出函数
window.components = {
    renderDepartmentCards,
    renderDoctorCards,
    renderCostDetail,
    showResultCard,
    hideResultCard,
};
