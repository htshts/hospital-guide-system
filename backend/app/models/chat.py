from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    """聊天消息模型"""
    role: str = Field(..., description="消息角色：user 或 assistant")
    content: str = Field(..., description="消息内容")
    timestamp: datetime = Field(default_factory=datetime.now, description="消息时间戳")

class ChatRequest(BaseModel):
    """聊天请求模型"""
    session_id: str = Field(..., description="会话ID")
    message: str = Field(..., description="用户消息")

class ChatResponse(BaseModel):
    """聊天响应模型"""
    session_id: str = Field(..., description="会话ID")
    message: ChatMessage = Field(..., description="AI回复消息")
    departments: Optional[List[Dict[str, Any]]] = Field(None, description="推荐的科室列表")
    doctors: Optional[List[Dict[str, Any]]] = Field(None, description="推荐的医生列表")
    cost: Optional[Dict[str, Any]] = Field(None, description="费用估算")

class SessionCreateRequest(BaseModel):
    """创建会话请求"""
    pass

class SessionResponse(BaseModel):
    """会话响应"""
    session_id: str = Field(..., description="会话ID")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
