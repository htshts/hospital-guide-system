from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
import json
import os

from app.models.response import CostEstimateRequest, CostEstimateResponse

router = APIRouter()

# 加载费用医保数据
def load_cost_insurance():
    """加载费用医保数据"""
    data_path = os.path.join(os.path.dirname(__file__), "../data/cost_insurance.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.post("/estimate", response_model=CostEstimateResponse)
async def estimate_cost(request: CostEstimateRequest):
    """
    估算费用
    
    逻辑：
    1. 根据科室获取常见检查项目及价格
    2. 计算总费用
    3. 根据医保政策计算报销金额
    """
    try:
        data = load_cost_insurance()
        dept_data = data.get("departments", {}).get(request.department)
        
        if not dept_data:
            # 如果没有找到该科室的数据，返回默认估算
            return CostEstimateResponse(
                total=300,
                insurance_pay=210,
                self_pay=90,
                breakdown=[{"name": "挂号费", "price": 50, "insurance_rate": 0.8}],
                insurance_policy=data.get("insurance_policy", {}).get("description")
            )
        
        # 计算费用
        breakdown = dept_data.get("common_procedures", [])
        total = sum(item["price"] for item in breakdown)
        
        # 计算医保支付
        insurance_pay = sum(
            item["price"] * item.get("insurance_rate", 0.7)
            for item in breakdown
        )
        self_pay = total - insurance_pay
        
        return CostEstimateResponse(
            total=round(total, 2),
            insurance_pay=round(insurance_pay, 2),
            self_pay=round(self_pay, 2),
            breakdown=breakdown,
            insurance_policy=data.get("insurance_policy", {}).get("description")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"费用估算失败: {str(e)}")
