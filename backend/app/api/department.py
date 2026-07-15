from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
import json
import os

from app.models.response import DepartmentRecommendRequest, DepartmentRecommendResponse

router = APIRouter()

# 加载科室数据
def load_departments():
    """加载科室数据"""
    data_path = os.path.join(os.path.dirname(__file__), "../data/departments.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 加载症状-疾病映射
def load_symptom_disease():
    """加载症状到疾病映射"""
    data_path = os.path.join(os.path.dirname(__file__), "../data/symptom_disease.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.post("/recommend", response_model=DepartmentRecommendResponse)
async def recommend_department(request: DepartmentRecommendRequest):
    """
    根据症状描述推荐科室
    
    逻辑：
    1. 从症状描述中提取关键词
    2. 匹配症状-疾病映射
    3. 根据疾病匹配科室
    4. 计算置信度排名
    """
    try:
        # 加载数据
        departments = load_departments()
        symptom_disease_map = load_symptom_disease()
        
        # 提取症状关键词（简单分词）
        symptoms = []
        # request.symptoms 是字符串，检查哪些症状关键词出现在描述中
        for symptom in symptom_disease_map.keys():
            if symptom in request.symptoms:
                symptoms.append(symptom)
        
        # 如果没有匹配到确切症状，尝试分词
        if not symptoms:
            # 简单分词：按逗号、空格、顿号分割
            import re
            words = re.split(r'[,，、\s]+', request.symptoms)
            for word in words:
                word = word.strip()
                if word and word in symptom_disease_map:
                    symptoms.append(word)
        
        if not symptoms:
            # 如果没有匹配到症状，返回所有科室
            return DepartmentRecommendResponse(
                departments=[{
                    "name": dept["name"],
                    "confidence": 0.5,
                    "reason": "未识别到具体症状，请详细描述您的症状"
                } for dept in departments[:3]]
            )
        
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
                "reason": f"根据您描述的症状，可能患有{'、'.join(info['diseases'][:3])}等疾病，建议就诊{dept_name}"
            })
        
        # 如果没有匹配到科室，添加默认推荐
        if not results:
            results.append({
                "name": "神经内科",
                "confidence": 0.6,
                "reason": "根据常见症状，建议先到神经内科就诊"
            })
        
        # 按置信度排序
        results.sort(key=lambda x: x["confidence"], reverse=True)
        
        return DepartmentRecommendResponse(
            departments=results[:3],
            reason=f"根据您描述的症状（{','.join(symptoms)}），为您推荐以下科室"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"科室推荐失败: {str(e)}")
