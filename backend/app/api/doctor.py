from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
import json
import os

from app.models.response import DoctorQueryResponse

router = APIRouter()

# 加载医生数据
def load_doctors():
    """加载医生数据"""
    data_path = os.path.join(os.path.dirname(__file__), "../data/doctors.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("", response_model=DoctorQueryResponse)
async def query_doctors(
    department: str = Query(..., description="科室名称"),
    schedule_day: Optional[str] = Query(None, description="排班日期（如：周一、周二）")
):
    """
    查询医生
    
    参数：
    - department: 科室名称
    - schedule_day: 排班日期（可选）
    """
    try:
        doctors = load_doctors()
        
        # 过滤科室
        filtered = [doc for doc in doctors if doc["department"] == department]
        
        if not filtered:
            # 如果没有找到 exact match，尝试模糊匹配
            for doc in doctors:
                if department in doc["department"] or doc["department"] in department:
                    filtered.append(doc)
        
        # 过滤排班
        if schedule_day:
            filtered = [
                doc for doc in filtered
                if schedule_day in doc.get("schedule", {})
            ]
        
        # 按评分排序
        filtered.sort(key=lambda x: x.get("rating", 0), reverse=True)
        
        return DoctorQueryResponse(doctors=filtered)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询医生失败: {str(e)}")
