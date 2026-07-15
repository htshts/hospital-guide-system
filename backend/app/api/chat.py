from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from typing import Dict, Any, AsyncGenerator
import json
import os
import asyncio

from app.models.chat import ChatRequest, ChatResponse, SessionResponse
from app.api.department import load_departments, load_symptom_disease

router = APIRouter()

# 内存会话存储
sessions: Dict[str, Dict[str, Any]] = {}

def get_session_manager():
    """获取会话管理器（简单内存版本）"""
    return sessions

@router.post("/session", response_model=SessionResponse)
async def create_session():
    """创建新会话"""
    import uuid
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "messages": [],
        "created_at": asyncio.get_event_loop().time()
    }
    return SessionResponse(session_id=session_id)

@router.post("/send")
async def send_message(request: ChatRequest):
    """
    发送消息（非流式）
    
    逻辑：
    1. 获取会话历史
    2. 分析用户症状
    3. 推荐科室
    4. 返回响应
    """
    try:
        # 获取会话
        session = sessions.get(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        # 添加用户消息到历史
        user_message = {"role": "user", "content": request.message}
        session["messages"].append(user_message)
        
        # 分析症状并推荐科室
        departments = analyze_symptoms(request.message)
        
        # 生成 AI 回复
        ai_response = generate_response(request.message, departments)
        
        # 添加 AI 回复到历史
        ai_message = {"role": "assistant", "content": ai_response}
        session["messages"].append(ai_message)
        
        return {
            "session_id": request.session_id,
            "message": ai_message,
            "departments": departments
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"发送消息失败: {str(e)}")

@router.get("/stream")
async def stream_message(session_id: str, message: str):
    """
    发送消息（SSE 流式响应）
    
    返回 Server-Sent Events 流
    """
    try:
        # 获取会话
        session = sessions.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        # 添加用户消息到历史
        user_message = {"role": "user", "content": message}
        session["messages"].append(user_message)
        
        # 分析症状并推荐科室
        departments = analyze_symptoms(message)
        
        # 生成 AI 回复（流式）
        ai_response = generate_response(message, departments)
        
        # 返回 SSE 流
        async def generate_sse():
            # 发送开始标记
            yield f"data: {json.dumps({'type': 'start'})}\n\n"
            
            # 流式发送回复（逐字）
            full_response = ai_response
            for i in range(len(full_response)):
                chunk = full_response[i]
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
                await asyncio.sleep(0.02)  # 模拟打字机效果
            
            # 发送科室推荐卡片
            if departments:
                yield f"data: {json.dumps({'type': 'departments', 'data': departments})}\n\n"
            
            # 发送结束标记
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            
            # 添加 AI 回复到历史
            ai_message = {"role": "assistant", "content": full_response}
            session["messages"].append(ai_message)
        
        return StreamingResponse(
            generate_sse(),
            media_type="text/event-stream"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"流式响应失败: {str(e)}")

def analyze_symptoms(message: str) -> list:
    """
    分析症状并推荐科室（简化版本）
    
    后续可升级为 LLM 推理版本
    """
    try:
        departments = load_departments()
        symptom_disease_map = load_symptom_disease()
        
        # 提取症状关键词
        symptoms = []
        for symptom in symptom_disease_map.keys():
            if symptom in message:
                symptoms.append(symptom)
        
        if not symptoms:
            return []
        
        # 统计疾病出现次数
        disease_count = {}
        for symptom in symptoms:
            if symptom in symptom_disease_map:
                for disease in symptom_disease_map[symptom]:
                    disease_count[disease] = disease_count.get(disease, 0) + 1
        
        # 根据疾病匹配科室
        dept_score = {}
        for disease, count in disease_count.items():
            for dept in departments:
                if disease in dept.get("common_diseases", []):
                    if dept["name"] not in dept_score:
                        dept_score[dept["name"]] = {"score": 0, "diseases": []}
                    dept_score[dept["name"]]["score"] += count
                    dept_score[dept["name"]]["diseases"].append(disease)
        
        # 计算置信度并排序
        results = []
        for dept_name, info in dept_score.items():
            confidence = min(0.95, 0.6 + info["score"] * 0.1)
            results.append({
                "name": dept_name,
                "confidence": round(confidence, 2),
                "reason": f"根据您描述的症状，可能患有{'、'.join(info['diseases'][:3])}等疾病"
            })
        
        # 按置信度排序
        results.sort(key=lambda x: x["confidence"], reverse=True)
        
        return results[:3]
        
    except Exception as e:
        print(f"分析症状失败: {e}")
        return []

def generate_response(message: str, departments: list) -> str:
    """
    生成 AI 回复（简化版本）
    
    后续可升级为 LLM 生成版本
    """
    if not departments:
        return "您好！请详细描述您的症状，我会帮您推荐合适的科室和医生。"
    
    response = f"根据您描述的症状，我为您推荐以下科室：\n\n"
    
    for i, dept in enumerate(departments, 1):
        response += f"{i}. **{dept['name']}**（置信度：{dept['confidence']*100:.0f}%）\n"
        response += f"   {dept.get('reason', '')}\n"
        
        # 查找科室描述
        try:
            all_depts = load_departments()
            for d in all_depts:
                if d["name"] == dept["name"]:
                    response += f"   科室介绍：{d.get('description', '')}\n"
                    break
        except:
            pass
    
    response += "\n您是否需要查询该科室的医生排班和费用估算？"
    
    return response
