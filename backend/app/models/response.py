from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class DepartmentRecommendRequest(BaseModel):
    """科室推荐请求"""
    symptoms: str = Field(..., description="症状描述")

class DepartmentRecommendResponse(BaseModel):
    """科室推荐响应"""
    departments: List[Dict[str, Any]] = Field(..., description="推荐的科室列表")
    reason: Optional[str] = Field(None, description="推荐理由")

class DoctorQueryRequest(BaseModel):
    """医生查询请求"""
    department: str = Field(..., description="科室名称")
    schedule_day: Optional[str] = Field(None, description="排班日期（如：周一、周二）")

class DoctorQueryResponse(BaseModel):
    """医生查询响应"""
    doctors: List[Dict[str, Any]] = Field(..., description="医生列表")

class CostEstimateRequest(BaseModel):
    """费用估算请求"""
    department: str = Field(..., description="科室名称")
    procedures: Optional[List[str]] = Field(None, description="指定检查项目")

class CostEstimateResponse(BaseModel):
    """费用估算响应"""
    total: float = Field(..., description="总费用")
    insurance_pay: float = Field(..., description="医保支付")
    self_pay: float = Field(..., description="自费金额")
    breakdown: List[Dict[str, Any]] = Field(..., description="费用明细")
    insurance_policy: Optional[str] = Field(None, description="医保政策说明")
