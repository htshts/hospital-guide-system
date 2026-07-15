#!/bin/bash
# 启动脚本 - 医院智能导诊系统

echo "正在启动医院智能导诊系统..."

# 检查是否在项目根目录
if [ ! -d "backend" ]; then
    echo "错误：请在项目根目录（ResumeP2）中运行此脚本"
    exit 1
fi

# 检查 Python 虚拟环境
if [ ! -d "backend/venv" ]; then
    echo "创建 Python 虚拟环境..."
    cd backend
    python -m venv venv
    cd ..
fi

# 检查依赖是否安装
echo "检查 Python 依赖..."
cd backend
./venv/Scripts/pip.exe install -r requirements.txt -q
cd ..

# 启动后端服务器
echo "启动后端服务器（http://localhost:8000）..."
echo "请在浏览器中打开 http://localhost:8000 访问系统"
echo "按 Ctrl+C 停止服务器"
echo ""

cd backend
./venv/Scripts/uvicorn.exe app.main:app --reload --host 0.0.0.0 --port 8000
