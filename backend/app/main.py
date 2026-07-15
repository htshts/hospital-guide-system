from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# 触发重新加载（添加调试输出）

app = FastAPI(
    title="医院智能导诊系统 API",
    description="基于 ReAct 与 RAG 的医院智能导诊问答系统",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 前端静态文件服务（从 backend/static/ 目录）
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
static_path = os.path.abspath(static_path)

print(f"DEBUG: static_path = {static_path}")
print(f"DEBUG: static_path exists = {os.path.exists(static_path)}")

if os.path.exists(static_path):
    # 服务静态文件（CSS、JS、图片等）
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    
    # 根路径服务前端页面
    @app.get("/")
    async def root():
        return FileResponse(os.path.join(static_path, "index.html"))
else:
    @app.get("/")
    async def root():
        return {
            "message": "医院智能导诊系统 API",
            "version": "1.0.0",
            "endpoints": {
                "docs": "/docs",
                "chat": "/api/v1/chat",
                "department": "/api/v1/department",
                "doctors": "/api/v1/doctors",
                "cost": "/api/v1/cost"
            }
        }

# 导入路由
from app.api import chat, department, doctor, cost
app.include_router(chat.router, prefix="/api/v1/chat", tags=["对话管理"])
app.include_router(department.router, prefix="/api/v1/department", tags=["科室推荐"])
app.include_router(doctor.router, prefix="/api/v1/doctors", tags=["医生查询"])
app.include_router(cost.router, prefix="/api/v1/cost", tags=["费用医保"])
