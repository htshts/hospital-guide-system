# 医院智能导诊系统 - 从零搭建完整教程

> 本教程将手把手教你从零开始搭建一个完整的医院智能导诊问答系统。无需任何前置项目经验，跟着做就能跑起来。

---

## 目录

- [第 0 章：项目介绍与学习目标](#第-0-章项目介绍与学习目标)
- [第 1 章：环境准备](#第-1-章环境准备)
- [第 2 章：后端 - 数据模型定义](#第-2-章后端---数据模型定义)
- [第 3 章：后端 - 示例数据准备](#第-3-章后端---示例数据准备)
- [第 4 章：后端 - API 端点实现（核心）](#第-4-章后端---api-端点实现核心)
- [第 5 章：后端 - 主入口与启动](#第-5-章后端---主入口与启动)
- [第 6 章：前端 - 界面实现](#第-6-章前端---界面实现)
- [第 7 章：联调与运行](#第-7-章联调与运行)
- [第 8 章：Docker 部署（可选）](#第-8-章docker-部署可选)
- [第 9 章：进阶指引](#第-9-章进阶指引)
- [附录](#附录)

---

## 第 0 章：项目介绍与学习目标

### 0.1 这个项目是什么？

这是一个**医院智能导诊问答系统**。用户在网页上输入症状描述（比如"头痛、恶心"），系统会：

1. **智能推荐科室** — 根据症状匹配可能的疾病，再推荐对应的科室
2. **查询医生排班** — 显示该科室的医生列表、职称、专长、排班时间
3. **估算就诊费用** — 计算常见检查项目的总费用和医保报销金额

最终效果：用户打开浏览器，输入症状，右侧自动显示科室推荐、医生信息和费用估算。

### 0.2 技术栈一览

| 层级 | 技术 | 作用 |
|------|------|------|
| 后端框架 | FastAPI (Python) | 提供 API 接口 |
| 数据验证 | Pydantic | 定义请求/响应的数据格式 |
| 数据存储 | JSON 文件 | 存储科室、医生、症状、费用数据 |
| 前端 | 纯 HTML + CSS + JavaScript | 用户界面（无需框架） |
| 通信方式 | fetch API | 前后端数据交互 |
| 服务器 | Uvicorn | 运行 FastAPI 应用 |

### 0.3 系统架构图

```
┌─────────────────────────────────────────────────────┐
│                    浏览器（用户端）                    │
│  ┌─────────────┐     ┌──────────────────────────┐  │
│  │  对话窗口    │     │    推荐结果区域           │  │
│  │  (输入症状)  │     │  科室卡 / 医生卡 / 费用卡  │  │
│  └─────────────┘     └──────────────────────────┘  │
└────────────────────────┬────────────────────────────┘
                         │ fetch 请求
                         ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI 后端 (localhost:8000)            │
│                                                      │
│  ┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────────┐ │
│  │科室推荐API│ │医生查询API│ │费用API │ │ 对话API  │ │
│  └────┬─────┘ └────┬─────┘ └───┬────┘ └────┬─────┘ │
│       │            │           │            │       │
│       ▼            ▼           ▼            ▼       │
│  ┌──────────────────────────────────────────────┐   │
│  │          JSON 数据文件 (data/*.json)          │   │
│  │  科室数据 / 医生数据 / 症状映射 / 费用医保     │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### 0.4 学完你能掌握什么？

- FastAPI 框架的基本使用（路由、模型、中间件）
- Pydantic 数据验证模型的写法
- Python 如何读写 JSON 文件
- 纯 HTML/CSS/JS 前端开发（无框架依赖）
- 前后端分离的通信方式（fetch API）
- CORS 跨域问题的解决
- 静态文件服务配置
- Docker 容器化部署基础

---

## 第 1 章：环境准备

### 1.1 安装 Python

> FastAPI 需要 Python 3.8+，推荐使用 3.10 或更高版本。

**Windows：**
1. 访问 https://www.python.org/downloads/ 下载 Python 3.10+
2. 安装时**勾选 "Add Python to PATH"**（非常重要！）
3. 安装完成后，打开命令提示符（CMD），输入：

```bash
python --version
```

如果显示 `Python 3.10.x` 或更高，说明安装成功。

**Mac/Linux：**
```bash
# Mac (使用 Homebrew)
brew install python@3.10

# Ubuntu/Debian
sudo apt update && sudo apt install python3.10 python3.10-venv

# 验证
python3 --version
```

### 1.2 创建项目目录

打开终端（Windows 用 CMD 或 PowerShell，Mac/Linux 用 Terminal），创建项目目录：

```bash
# 创建项目根目录
mkdir hospital-guide-system
cd hospital-guide-system

# 创建后端目录结构
mkdir -p backend/app/api
mkdir -p backend/app/models
mkdir -p backend/app/data
mkdir -p backend/static

# 创建前端目录结构
mkdir -p frontend/css
mkdir -p frontend/js
```

> **什么是 `__init__.py`？** 在 Python 中，包含 `__init__.py` 文件的目录被称为"包"（package）。这个文件告诉 Python 这个目录是一个可导入的模块。文件可以是空的，但它必须存在。

创建空的 `__init__.py` 文件：

**Windows (CMD)：**
```cmd
type nul > backend\app\__init__.py
type nul > backend\app\api\__init__.py
type nul > backend\app\models\__init__.py
```

**Mac/Linux：**
```bash
touch backend/app/__init__.py
touch backend/app/api/__init__.py
touch backend/app/models/__init__.py
```

### 1.3 创建虚拟环境

> **什么是虚拟环境？** 虚拟环境是一个独立的 Python 运行环境。它让你为每个项目单独安装依赖包，不会污染系统全局的 Python 环境。比如项目 A 需要 FastAPI 0.115，项目 B 需要 FastAPI 0.100，虚拟环境让它们互不干扰。

```bash
# 进入 backend 目录
cd backend

# 创建虚拟环境
# Windows:
python -m venv venv
# Mac/Linux:
python3 -m venv venv

# 激活虚拟环境
# Windows (CMD):
venv\Scripts\activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate
```

激活成功后，终端前面会出现 `(venv)` 字样，表示你已经在虚拟环境中了。

### 1.4 安装依赖

创建 `backend/requirements.txt` 文件，内容如下：

```txt
# FastAPI 框架
fastapi>=0.115.0
uvicorn[standard]>=0.34.0

# LangChain 相关（后续进阶用，基础版可不装）
langchain>=0.3.0
langchain-community>=0.3.0
langchain-openai>=0.2.0

# Milvus 向量数据库（后续进阶用，基础版可不装）
pymilvus>=2.5.0

# OpenAI API（后续进阶用，基础版可不装）
openai>=1.60.0

# 数据处理
pydantic>=2.10.0
pydantic-settings>=2.7.0
python-dotenv>=1.0.0
pyyaml>=6.0.0

# 备用向量计算（如 Milvus 不可用时）
scikit-learn>=1.6.0
numpy>=2.1.0

# HTTP 请求
requests>=2.32.0
```

> **每个包的作用：**
> - `fastapi`：Web 框架，用来写 API 接口
> - `uvicorn`：ASGI 服务器，用来运行 FastAPI 应用
> - `pydantic`：数据验证库，FastAPI 自带依赖，用于定义数据模型
> - `python-dotenv`：读取 `.env` 环境变量文件
> - `requests`：HTTP 请求库，用于测试 API
> - 其他 LangChain/Milvus/OpenAI 包是进阶功能用的，基础版可以先不装

安装依赖：

```bash
# 确保已激活虚拟环境，然后在 backend 目录下执行
pip install -r requirements.txt

# 如果下载慢，使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 1.5 验证安装

```bash
python -c "import fastapi; print(f'FastAPI 版本: {fastapi.__version__}')"
```

如果输出 FastAPI 版本号，说明安装成功。

### ✅ 本章验证

完成本章后，你的目录结构应该是：

```
hospital-guide-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   └── __init__.py
│   │   └── data/
│   ├── static/
│   ├── requirements.txt
│   └── venv/              # 虚拟环境目录
└── frontend/
    ├── css/
    └── js/
```

---

## 第 2 章：后端 - 数据模型定义

### 2.1 什么是 Pydantic？

> Pydantic 是 Python 的数据验证库。它让你用 Python 类来定义数据结构，自动验证传入的数据是否符合要求。FastAPI 内置了 Pydantic，当你定义一个 Pydantic 模型类，FastAPI 会自动：
> 1. 验证请求体是否符合模型定义
> 2. 生成 API 文档（Swagger UI）
> 3. 将 Python 对象自动转换为 JSON 响应

简单来说，Pydantic 模型就是**数据的合同**，规定了"这个 API 接收什么格式的数据，返回什么格式的数据"。

### 2.2 创建聊天模型 `app/models/chat.py`

创建文件 `backend/app/models/chat.py`，内容如下：

```python
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
```

**代码讲解：**

- `BaseModel`：Pydantic 的基类，所有模型都继承它
- `Field(..., description="...")`：`...` 表示该字段是必填的，`description` 是字段说明（会显示在 API 文档中）
- `Optional[xxx] = Field(None)`：表示该字段是可选的，默认值为 `None`
- `default_factory=datetime.now`：表示该字段默认值为当前时间（每次创建对象时自动生成）
- `List[Dict[str, Any]]`：表示"字典列表"，例如 `[{"name": "内科"}, {"name": "外科"}]`

### 2.3 创建响应模型 `app/models/response.py`

创建文件 `backend/app/models/response.py`，内容如下：

```python
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
```

**代码讲解：**

这个文件定义了 4 个 API 的请求和响应模型：

| API | 请求模型 | 响应模型 |
|-----|---------|---------|
| 科室推荐 | `DepartmentRecommendRequest` | `DepartmentRecommendResponse` |
| 医生查询 | `DoctorQueryRequest` | `DoctorQueryResponse` |
| 费用估算 | `CostEstimateRequest` | `CostEstimateResponse` |
| 聊天对话 | `ChatRequest` | `ChatResponse` |

### ✅ 本章验证

在 `backend` 目录下运行：

```bash
python -c "from app.models.chat import ChatRequest; print('模型导入成功')"
python -c "from app.models.response import DepartmentRecommendRequest; print('模型导入成功')"
```

如果输出"模型导入成功"，说明模型定义正确。

---

## 第 3 章：后端 - 示例数据准备

### 3.1 为什么用 JSON 而不是数据库？

在这个项目中，我们使用 JSON 文件存储数据，原因如下：

1. **简单**：无需安装和配置数据库（MySQL、PostgreSQL 等）
2. **易读**：JSON 是纯文本格式，直接打开就能看
3. **够用**：示例数据量小（10 个科室、10 个医生），JSON 完全够用
4. **易替换**：后续要换成数据库时，只需修改数据加载函数

### 3.2 科室数据 `app/data/departments.json`

创建文件 `backend/app/data/departments.json`，内容如下：

```json
[
  {
    "id": "dept_001",
    "name": "神经内科",
    "description": "诊治脑血管疾病、癫痫、帕金森病、偏头痛、神经痛等神经系统疾病",
    "symptoms": ["头痛", "头晕", "眩晕", "肢体麻木", "抽搐", "记忆力下降", "失眠"],
    "common_diseases": ["偏头痛", "癫痫", "帕金森病", "脑梗死", "脑出血", "面瘫"]
  },
  {
    "id": "dept_002",
    "name": "心血管内科",
    "description": "诊治高血压、冠心病、心律失常、心力衰竭等心血管疾病",
    "symptoms": ["胸痛", "胸闷", "心悸", "气短", "下肢水肿", "高血压"],
    "common_diseases": ["高血压", "冠心病", "心律失常", "心力衰竭", "心肌梗死"]
  },
  {
    "id": "dept_003",
    "name": "呼吸内科",
    "description": "诊治呼吸道感染、慢性阻塞性肺疾病、哮喘、肺炎等呼吸系统疾病",
    "symptoms": ["咳嗽", "咳痰", "呼吸困难", "胸痛", "发热", "咳血"],
    "common_diseases": ["感冒", "肺炎", "哮喘", "慢性阻塞性肺疾病", "支气管炎"]
  },
  {
    "id": "dept_004",
    "name": "消化内科",
    "description": "诊治胃炎、胃溃疡、肝炎、肠易激综合征等消化系统疾病",
    "symptoms": ["腹痛", "腹胀", "恶心", "呕吐", "腹泻", "便秘", "食欲不振"],
    "common_diseases": ["胃炎", "胃溃疡", "肝炎", "胆囊炎", "肠炎", "消化不良"]
  },
  {
    "id": "dept_005",
    "name": "骨科",
    "description": "诊治骨折、关节炎、腰椎间盘突出、骨质疏松等骨骼肌肉系统疾病",
    "symptoms": ["关节疼痛", "腰背痛", "骨折", "肢体活动障碍", "肌肉疼痛"],
    "common_diseases": ["骨折", "骨关节炎", "腰椎间盘突出", "骨质疏松", "颈椎病"]
  },
  {
    "id": "dept_006",
    "name": "内分泌科",
    "description": "诊治糖尿病、甲状腺疾病、骨质疏松等内分泌代谢疾病",
    "symptoms": ["多饮多尿", "体重异常变化", "心悸", "怕热多汗", "乏力"],
    "common_diseases": ["糖尿病", "甲状腺功能亢进", "甲状腺功能减退", "痛风"]
  },
  {
    "id": "dept_007",
    "name": "皮肤科",
    "description": "诊治湿疹、皮炎、荨麻疹、痤疮、带状疱疹等皮肤疾病",
    "symptoms": ["皮疹", "瘙痒", "皮肤红肿", "脱屑", "水疱"],
    "common_diseases": ["湿疹", "皮炎", "荨麻疹", "痤疮", "带状疱疹", "真菌感染"]
  },
  {
    "id": "dept_008",
    "name": "眼科",
    "description": "诊治结膜炎、白内障、青光眼、近视等眼部疾病",
    "symptoms": ["眼红", "眼痛", "视力下降", "眼痒", "流泪"],
    "common_diseases": ["结膜炎", "白内障", "青光眼", "近视", "干眼症"]
  },
  {
    "id": "dept_009",
    "name": "耳鼻喉科",
    "description": "诊治鼻炎、扁桃体炎、中耳炎等耳鼻喉疾病",
    "symptoms": ["鼻塞", "流涕", "咽痛", "耳鸣", "听力下降", "咽喉异物感"],
    "common_diseases": ["鼻炎", "扁桃体炎", "中耳炎", "咽炎", "鼻窦炎"]
  },
  {
    "id": "dept_010",
    "name": "泌尿外科",
    "description": "诊治尿路感染、肾结石、前列腺增生等泌尿系统疾病",
    "symptoms": ["尿频", "尿急", "尿痛", "腰痛", "血尿"],
    "common_diseases": ["尿路感染", "肾结石", "前列腺炎", "前列腺增生"]
  }
]
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 科室唯一标识 |
| `name` | string | 科室名称 |
| `description` | string | 科室介绍 |
| `symptoms` | array | 该科室常见症状列表 |
| `common_diseases` | array | 该科室常见疾病列表（用于症状→疾病→科室的匹配） |

### 3.3 医生数据 `app/data/doctors.json`

创建文件 `backend/app/data/doctors.json`，内容如下：

```json
[
  {
    "id": "doc_001",
    "name": "张明华",
    "department": "神经内科",
    "title": "主任医师",
    "specialty": "偏头痛、癫痫、帕金森病",
    "schedule": {
      "周一": "上午",
      "周三": "全天",
      "周五": "上午"
    },
    "rating": 4.9,
    "experience_years": 25,
    "introduction": "擅长神经系统疾病的诊治，尤其在偏头痛和癫痫的诊疗方面有丰富经验。"
  },
  {
    "id": "doc_002",
    "name": "李芳",
    "department": "神经内科",
    "title": "副主任医师",
    "specialty": "脑梗死、脑出血、眩晕",
    "schedule": {
      "周二": "全天",
      "周四": "上午",
      "周六": "上午"
    },
    "rating": 4.7,
    "experience_years": 15,
    "introduction": "专注于脑血管疾病的诊治，对眩晕症的鉴别诊断有独到见解。"
  },
  {
    "id": "doc_003",
    "name": "王强",
    "department": "心血管内科",
    "title": "主任医师",
    "specialty": "高血压、冠心病、心力衰竭",
    "schedule": {
      "周一": "全天",
      "周三": "上午",
      "周四": "全天"
    },
    "rating": 4.8,
    "experience_years": 22,
    "introduction": "心血管内科专家，擅长复杂冠心病的介入治疗。"
  },
  {
    "id": "doc_004",
    "name": "赵敏",
    "department": "心血管内科",
    "title": "副主任医师",
    "specialty": "心律失常、心悸",
    "schedule": {
      "周二": "上午",
      "周五": "全天"
    },
    "rating": 4.6,
    "experience_years": 12,
    "introduction": "擅长心律失常的药物治疗和导管消融术。"
  },
  {
    "id": "doc_005",
    "name": "刘伟",
    "department": "呼吸内科",
    "title": "主任医师",
    "specialty": "肺炎、哮喘、慢性阻塞性肺病",
    "schedule": {
      "周一": "上午",
      "周三": "全天",
      "周五": "上午"
    },
    "rating": 4.7,
    "experience_years": 20,
    "introduction": "呼吸系统感染性疾病专家，对哮喘的长期管理有丰富经验。"
  },
  {
    "id": "doc_006",
    "name": "陈静",
    "department": "消化内科",
    "title": "主任医师",
    "specialty": "胃炎、胃溃疡、肝炎",
    "schedule": {
      "周二": "全天",
      "周四": "全天",
      "周六": "上午"
    },
    "rating": 4.8,
    "experience_years": 18,
    "introduction": "消化内镜专家，擅长早期胃癌和食管癌的内镜下诊治。"
  },
  {
    "id": "doc_007",
    "name": "孙立",
    "department": "骨科",
    "title": "主任医师",
    "specialty": "骨折、骨关节炎、腰椎间盘突出",
    "schedule": {
      "周一": "全天",
      "周三": "上午",
      "周五": "全天"
    },
    "rating": 4.9,
    "experience_years": 28,
    "introduction": "骨科专家，擅长关节置换术和脊柱微创手术。"
  },
  {
    "id": "doc_008",
    "name": "周婷",
    "department": "内分泌科",
    "title": "副主任医师",
    "specialty": "糖尿病、甲状腺疾病",
    "schedule": {
      "周二": "全天",
      "周四": "上午",
      "周五": "上午"
    },
    "rating": 4.7,
    "experience_years": 14,
    "introduction": "内分泌代谢疾病专家，对糖尿病的个体化治疗有深入研究。"
  },
  {
    "id": "doc_009",
    "name": "吴刚",
    "department": "皮肤科",
    "title": "主任医师",
    "specialty": "湿疹、皮炎、痤疮、带状疱疹",
    "schedule": {
      "周一": "全天",
      "周三": "全天",
      "周五": "上午"
    },
    "rating": 4.6,
    "experience_years": 19,
    "introduction": "皮肤性病专家，擅长过敏性皮肤病和病毒性皮肤病的诊治。"
  },
  {
    "id": "doc_010",
    "name": "郑秀英",
    "department": "眼科",
    "title": "主任医师",
    "specialty": "结膜炎、白内障、青光眼",
    "schedule": {
      "周二": "全天",
      "周四": "全天"
    },
    "rating": 4.8,
    "experience_years": 23,
    "introduction": "眼科专家，擅长白内障超声乳化手术和青光眼手术。"
  }
]
```

### 3.4 症状-疾病映射 `app/data/symptom_disease.json`

创建文件 `backend/app/data/symptom_disease.json`，内容如下：

```json
{
  "头痛": ["偏头痛", "紧张性头痛", "高血压", "脑梗死", "脑出血"],
  "头晕": ["眩晕", "高血压", "脑梗死", "颈椎病"],
  "胸痛": ["冠心病", "心肌梗死", "高血压", "胃炎"],
  "咳嗽": ["感冒", "肺炎", "哮喘", "支气管炎", "慢性阻塞性肺病"],
  "腹痛": ["胃炎", "胃溃疡", "肠炎", "胆囊炎", "肾结石"],
  "关节痛": ["骨关节炎", "类风湿关节炎", "痛风", "骨折"],
  "皮疹": ["湿疹", "皮炎", "荨麻疹", "痤疮", "带状疱疹"],
  "眼红": ["结膜炎", "干眼症"],
  "鼻塞": ["鼻炎", "鼻窦炎", "感冒"],
  "咽痛": ["咽炎", "扁桃体炎", "感冒"],
  "多饮多尿": ["糖尿病"],
  "心悸": ["心律失常", "甲状腺功能亢进", "高血压"],
  "视力下降": ["白内障", "青光眼", "近视"],
  "耳鸣": ["中耳炎", "耳鸣症"],
  "尿频尿急": ["尿路感染", "前列腺炎", "前列腺增生"],
  "腰背痛": ["腰椎间盘突出", "骨质疏松", "腰肌劳损"]
}
```

**这个文件是科室推荐算法的核心。** 它的数据结构是：

```
症状 → [可能对应的疾病列表]
```

比如 `"头痛": ["偏头痛", "紧张性头痛", "高血压", "脑梗死", "脑出血"]` 表示"头痛"这个症状可能对应的 5 种疾病。

算法逻辑是：
1. 用户输入"我头痛3天了"
2. 系统检测到"头痛"这个关键词
3. 查到"头痛" → ["偏头痛", "紧张性头痛", "高血压", "脑梗死", "脑出血"]
4. 再去 `departments.json` 中查找哪些科室的 `common_diseases` 包含这些疾病
5. 匹配到"神经内科"（有偏头痛、癫痫等）和"心血管内科"（有高血压等）
6. 计算置信度，排序后返回推荐结果

### 3.5 费用医保数据 `app/data/cost_insurance.json`

创建文件 `backend/app/data/cost_insurance.json`，内容如下：

```json
{
  "departments": {
    "神经内科": {
      "common_procedures": [
        {"name": "头颅CT", "price": 250, "insurance_rate": 0.8},
        {"name": "头颅MRI", "price": 600, "insurance_rate": 0.7},
        {"name": "脑电图", "price": 150, "insurance_rate": 0.85},
        {"name": "挂号费", "price": 50, "insurance_rate": 0.8}
      ],
      "avg_total_cost": 500,
      "insurance_threshold": 1000,
      "insurance_ceiling": 50000
    },
    "心血管内科": {
      "common_procedures": [
        {"name": "心电图", "price": 30, "insurance_rate": 0.9},
        {"name": "心脏彩超", "price": 300, "insurance_rate": 0.75},
        {"name": "冠脉造影", "price": 4000, "insurance_rate": 0.6},
        {"name": "挂号费", "price": 50, "insurance_rate": 0.8}
      ],
      "avg_total_cost": 800,
      "insurance_threshold": 1000,
      "insurance_ceiling": 50000
    },
    "呼吸内科": {
      "common_procedures": [
        {"name": "胸部CT", "price": 300, "insurance_rate": 0.75},
        {"name": "肺功能检查", "price": 150, "insurance_rate": 0.85},
        {"name": "血常规", "price": 30, "insurance_rate": 0.9},
        {"name": "挂号费", "price": 40, "insurance_rate": 0.8}
      ],
      "avg_total_cost": 400,
      "insurance_threshold": 1000,
      "insurance_ceiling": 50000
    },
    "消化内科": {
      "common_procedures": [
        {"name": "胃镜", "price": 300, "insurance_rate": 0.7},
        {"name": "肠镜", "price": 400, "insurance_rate": 0.7},
        {"name": "幽门螺杆菌检测", "price": 100, "insurance_rate": 0.85},
        {"name": "挂号费", "price": 40, "insurance_rate": 0.8}
      ],
      "avg_total_cost": 600,
      "insurance_threshold": 1000,
      "insurance_ceiling": 50000
    },
    "骨科": {
      "common_procedures": [
        {"name": "X光片", "price": 80, "insurance_rate": 0.85},
        {"name": "CT三维重建", "price": 400, "insurance_rate": 0.7},
        {"name": "挂号费", "price": 50, "insurance_rate": 0.8}
      ],
      "avg_total_cost": 700,
      "insurance_threshold": 1000,
      "insurance_ceiling": 50000
    }
  },
  "insurance_policy": {
    "name": "城镇职工基本医疗保险",
    "threshold": 1000,
    "ceiling": 50000,
    "outpatient_rate": 0.7,
    "inpatient_rate": 0.85,
    "description": "起付线1000元，封顶线50000元，门诊报销70%，住院报销85%"
  }
}
```

**费用计算逻辑：**
- 总费用 = 所有检查项目 `price` 之和
- 医保支付 = 每个项目的 `price × insurance_rate` 之和
- 自费 = 总费用 - 医保支付

### ✅ 本章验证

在 `backend` 目录下运行：

```bash
python -c "import json; data = json.load(open('app/data/departments.json', encoding='utf-8')); print(f'科室数量: {len(data)}')"
```

如果输出"科室数量: 10"，说明数据文件创建正确。

---

## 第 4 章：后端 - API 端点实现（核心）

### 4.1 FastAPI 路由机制简介

> FastAPI 使用"路由器"（APIRouter）来组织 API。每个路由器负责一组相关的接口。比如：
> - `department.py` 负责科室推荐相关接口
> - `doctor.py` 负责医生查询相关接口
> - `cost.py` 负责费用估算相关接口
> - `chat.py` 负责对话管理相关接口
>
> 然后在 `main.py` 中把这些路由器"挂载"到主应用上，设置统一的 URL 前缀（如 `/api/v1/department`）。

### 4.2 科室推荐 API — `app/api/department.py`

创建文件 `backend/app/api/department.py`，内容如下：

```python
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
```

**算法逻辑详解：**

```
用户输入："我头痛3天了，有时候会恶心"

步骤1：提取症状关键词
  → 检查 symptom_disease.json 的 key
  → "头痛" 在输入中找到 ✓
  → 结果：symptoms = ["头痛"]

步骤2：查找症状对应的疾病
  → "头痛": ["偏头痛", "紧张性头痛", "高血压", "脑梗死", "脑出血"]
  → disease_count = {"偏头痛": 1, "紧张性头痛": 1, "高血压": 1, "脑梗死": 1, "脑出血": 1}

步骤3：根据疾病匹配科室
  → "偏头痛" 在 神经内科 的 common_diseases 中 ✓
  → "高血压" 在 心血管内科 的 common_diseases 中 ✓
  → dept_score = {
      "神经内科": {"score": 1, "diseases": ["偏头痛", "紧张性头痛", "脑梗死", "脑出血"]},
      "心血管内科": {"score": 1, "diseases": ["高血压"]}
    }

步骤4：计算置信度
  → 神经内科：min(0.95, 0.6 + 1 * 0.1) = 0.7
  → 心血管内科：min(0.95, 0.6 + 1 * 0.1) = 0.7

步骤5：排序并返回 Top 3
  → 返回 [{name: "神经内科", confidence: 0.7, ...}, {name: "心血管内科", confidence: 0.7, ...}]
```

### 4.3 医生查询 API — `app/api/doctor.py`

创建文件 `backend/app/api/doctor.py`，内容如下：

```python
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
```

**代码讲解：**

- `@router.get("")`：定义 GET 请求，路径为空字符串（因为会在 main.py 中设置前缀 `/api/v1/doctors`）
- `Query(...)`：`...` 表示该参数是必填的查询参数
- `Query(None)`：表示该参数是可选的
- 查询逻辑：先精确匹配科室名称，如果没有匹配到，再尝试模糊匹配

### 4.4 费用估算 API — `app/api/cost.py`

创建文件 `backend/app/api/cost.py`，内容如下：

```python
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
```

**费用计算示例：**

以呼吸内科为例：

| 项目 | 价格 | 医保报销比例 | 医保支付 |
|------|------|-------------|---------|
| 胸部CT | 300 | 75% | 225 |
| 肺功能检查 | 150 | 85% | 127.5 |
| 血常规 | 30 | 90% | 27 |
| 挂号费 | 40 | 80% | 32 |
| **合计** | **520** | | **411.5** |

- 总费用 = 300 + 150 + 30 + 40 = 520
- 医保支付 = 225 + 127.5 + 27 + 32 = 411.5
- 自费 = 520 - 411.5 = 108.5

### 4.5 对话管理 API — `app/api/chat.py`

创建文件 `backend/app/api/chat.py`，内容如下：

```python
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
```

**代码讲解：**

这个文件包含 3 个 API 端点和 2 个辅助函数：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/chat/session` | POST | 创建新会话，返回 session_id |
| `/api/v1/chat/send` | POST | 发送消息（非流式），返回完整响应 |
| `/api/v1/chat/stream` | GET | 发送消息（SSE 流式），逐字返回 |

**什么是 SSE（Server-Sent Events）？**

SSE 是一种服务器推送技术，允许服务器持续向客户端发送数据。与普通 HTTP 请求（请求→响应一次完成）不同，SSE 建立连接后，服务器可以不断推送数据，直到结束。这在"打字机效果"场景中非常有用——AI 的回复可以一个字一个字地显示，而不是等全部生成完才显示。

### ✅ 本章验证

在 `backend` 目录下运行：

```bash
python -c "from app.api.department import load_departments; print('API 模块导入成功')"
python -c "from app.api.chat import analyze_symptoms; print('对话模块导入成功')"
```

如果都输出"成功"，说明 API 代码编写正确。

---

## 第 5 章：后端 - 主入口与启动

### 5.1 创建主入口文件 `app/main.py`

创建文件 `backend/app/main.py`，内容如下：

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

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
```

**代码逐段讲解：**

**第1段：导入库**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 跨域中间件
from fastapi.staticfiles import StaticFiles          # 静态文件服务
from fastapi.responses import FileResponse           # 文件响应
```

**第2段：创建 FastAPI 应用**
```python
app = FastAPI(
    title="医院智能导诊系统 API",       # 显示在文档标题
    description="基于 ReAct 与 RAG...",  # API 描述
    version="1.0.0"                      # 版本号
)
```

**第3段：CORS 中间件**

> **什么是 CORS（跨域）？** 当前端运行在 `http://localhost:8080`，后端运行在 `http://localhost:8000` 时，浏览器出于安全原因会阻止前端访问后端（不同端口视为不同域）。CORS 中间件的作用是告诉浏览器"允许跨域访问"。
>
> `allow_origins=["*"]` 表示允许所有来源访问。生产环境中应该限制为你的前端域名，如 `["http://localhost:8080"]`。

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 允许所有来源
    allow_credentials=True,    # 允许携带凭证
    allow_methods=["*"],       # 允许所有 HTTP 方法
    allow_headers=["*"],       # 允许所有请求头
)
```

**第4段：静态文件服务**

这段代码让 FastAPI 可以直接服务前端文件（HTML/CSS/JS），这样你只需要启动后端就能访问前端页面，不用单独启动前端服务器。

```python
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
# static_path 指向 backend/static/ 目录
```

**第5段：路由注册**

将 4 个 API 路由器挂载到主应用上：

```python
app.include_router(chat.router, prefix="/api/v1/chat", ...)
# 最终路径：/api/v1/chat/session, /api/v1/chat/send, /api/v1/chat/stream

app.include_router(department.router, prefix="/api/v1/department", ...)
# 最终路径：/api/v1/department/recommend

app.include_router(doctor.router, prefix="/api/v1/doctors", ...)
# 最终路径：/api/v1/doctors

app.include_router(cost.router, prefix="/api/v1/cost", ...)
# 最终路径：/api/v1/cost/estimate
```

### 5.2 启动后端服务器

在 `backend` 目录下（确保虚拟环境已激活），运行：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**参数说明：**

| 参数 | 作用 |
|------|------|
| `app.main:app` | 指向 `app/main.py` 文件中的 `app` 变量 |
| `--reload` | 热重载，修改代码后自动重启服务器 |
| `--host 0.0.0.0` | 允许外部访问（不限于 localhost） |
| `--port 8000` | 监听 8000 端口 |

### 5.3 访问 API 文档

启动成功后，打开浏览器访问：

```
http://localhost:8000/docs
```

你会看到 FastAPI 自动生成的 Swagger UI 文档，包含所有 API 接口的说明和在线测试功能。

### 5.4 测试 API

用浏览器或 curl 测试科室推荐 API：

```bash
# 测试科室推荐
curl -X POST http://localhost:8000/api/v1/department/recommend ^
  -H "Content-Type: application/json" ^
  -d "{\"symptoms\": \"头痛、头晕\"}"

# Windows (CMD) 注意：JSON 中的引号需要转义
```

或者用 Python 测试：

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/department/recommend",
    json={"symptoms": "头痛、头晕"}
)
print(response.json())
```

### ✅ 本章验证

1. 启动后端服务器，终端应显示：
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete.
   ```

2. 访问 `http://localhost:8000/docs` 能看到 API 文档页面

---

## 第 6 章：前端 - 界面实现

### 6.1 前端架构设计

> **为什么用纯 HTML 而不用 React/Vue？**
>
> 1. **零构建**：不需要 Node.js、npm、webpack，直接写就能用
> 2. **易学**：HTML/CSS/JS 是前端基础，适合初学者
> 3. **够用**：这个项目界面简单，纯 JS 完全能实现
> 4. **易部署**：只需静态文件服务器即可

前端文件结构：

```
frontend/
├── index.html       # 主页面（HTML 结构）
├── css/
│   └── style.css    # 样式表
└── js/
    ├── utils.js      # 工具函数（DOM 操作等）
    ├── api.js        # API 请求封装
    ├── components.js # UI 组件渲染
    └── chat.js       # 对话逻辑（核心）
```

### 6.2 创建 HTML 页面 `frontend/index.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>医院智能导诊系统</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="app-container">
        <!-- 顶部标题栏 -->
        <header class="app-header">
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">🏥</span>
                    <h1>医院智能导诊系统</h1>
                </div>
                <div class="header-actions">
                    <button id="btn-clear" class="btn-secondary" title="清空对话">清空</button>
                </div>
            </div>
        </header>

        <!-- 主内容区 -->
        <main class="main-content">
            <!-- 左侧：对话区域 -->
            <section class="chat-section">
                <div class="chat-container">
                    <!-- 消息列表 -->
                    <div id="message-list" class="message-list">
                        <!-- 欢迎消息 -->
                        <div class="message assistant">
                            <div class="message-avatar">🤖</div>
                            <div class="message-content">
                                <div class="message-text">
                                    您好！我是医院智能导诊助手。<br>
                                    请描述您的症状，我会为您推荐合适的科室和医生。
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 输入区域 -->
                    <div class="input-section">
                        <div class="input-container">
                            <textarea 
                                id="user-input" 
                                class="user-input" 
                                placeholder="请描述您的症状，例如：发热、咳嗽、头痛..."
                                rows="2"
                            ></textarea>
                            <button id="btn-send" class="btn-primary">
                                <span class="btn-text">发送</span>
                                <span class="btn-loading" style="display:none;">发送中...</span>
                            </button>
                        </div>
                        <div class="input-hints">
                            <span class="hint-label">快速输入：</span>
                            <button class="hint-btn" data-text="发热、咳嗽">发热咳嗽</button>
                            <button class="hint-btn" data-text="头痛、头晕">头痛头晕</button>
                            <button class="hint-btn" data-text="腹痛、腹泻">腹痛腹泻</button>
                            <button class="hint-btn" data-text="关节痛">关节痛</button>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 右侧：推荐结果区域 -->
            <aside class="result-section">
                <!-- 科室推荐 -->
                <div class="result-card" id="department-result" style="display:none;">
                    <h3 class="result-title">
                        <span class="result-icon">📍</span>
                        推荐科室
                    </h3>
                    <div class="result-content" id="department-list"></div>
                </div>

                <!-- 医生推荐 -->
                <div class="result-card" id="doctor-result" style="display:none;">
                    <h3 class="result-title">
                        <span class="result-icon">👨‍⚕️</span>
                        推荐医生
                    </h3>
                    <div class="result-content" id="doctor-list"></div>
                </div>

                <!-- 费用估算 -->
                <div class="result-card" id="cost-result" style="display:none;">
                    <h3 class="result-title">
                        <span class="result-icon">💰</span>
                        费用估算
                    </h3>
                    <div class="result-content" id="cost-detail"></div>
                </div>

                <!-- 操作提示 -->
                <div class="help-card">
                    <h3 class="result-title">
                        <span class="result-icon">💡</span>
                        使用提示
                    </h3>
                    <ul class="help-list">
                        <li>描述症状时，尽量详细具体</li>
                        <li>可以一次描述多个症状</li>
                        <li>系统会推荐科室、医生和预估费用</li>
                        <li>点击推荐卡片可查看详细信息</li>
                    </ul>
                </div>
            </aside>
        </main>
    </div>

    <!-- 加载脚本（注意顺序！） -->
    <script src="js/utils.js"></script>
    <script src="js/api.js"></script>
    <script src="js/components.js"></script>
    <script src="js/chat.js"></script>
</body>
</html>
```

**布局讲解：**

```
┌─────────────────────────────────────────────────────┐
│  🏥 医院智能导诊系统              [清空]            │  ← 顶部标题栏
├─────────────────────────────────────────────────────┤
│                          │                          │
│  对话窗口                  │   推荐结果区域            │
│  ┌──────────────────┐    │  ┌──────────────────┐   │
│  │ 🤖 您好！我是...  │    │  │ 📍 推荐科室      │   │
│  │                  │    │  │ ┌──────────────┐ │   │
│  │ 👤 我头痛3天了    │    │  │ │ 神经内科 70% │ │   │
│  │                  │    │  │ └──────────────┘ │   │
│  │ 🤖 根据您的症状...│    │  └──────────────────┘   │
│  └──────────────────┘    │  ┌──────────────────┐   │
│  ┌──────────────────┐    │  │ 👨‍⚕️ 推荐医生      │   │
│  │输入症状...   [发送]│    │  │ 张明华 主任医师  │   │
│  └──────────────────┘    │  └──────────────────┘   │
│  [发热咳嗽][头痛头晕]...  │  ┌──────────────────┐   │
│                          │  │ 💰 费用估算      │   │
│                          │  │ 总520 医保411   │   │
│                          │  └──────────────────┘   │
└─────────────────────────────────────────────────────┘
```

> **注意脚本加载顺序！** `utils.js` 必须先加载（因为它定义了基础工具函数），然后是 `api.js`（依赖 utils），接着是 `components.js`（依赖 utils），最后是 `chat.js`（依赖以上所有）。

### 6.3 创建样式表 `frontend/css/style.css`

> 由于篇幅较长，这里给出完整代码。主要使用 CSS 变量（`:root`）定义颜色主题，使用 Flexbox 布局。

```css
/* 全局样式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #1890ff;
    --primary-hover: #40a9ff;
    --success-color: #52c41a;
    --warning-color: #faad14;
    --error-color: #f5222d;
    --text-primary: #262626;
    --text-secondary: #8c8c8c;
    --bg-primary: #f0f2f5;
    --bg-white: #ffffff;
    --border-color: #d9d9d9;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 2px 8px rgba(0,0,0,0.1);
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
}

/* 应用容器 */
.app-container {
    max-width: 1400px;
    margin: 0 auto;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* 顶部标题栏 */
.app-header {
    background: var(--bg-white);
    border-bottom: 1px solid var(--border-color);
    padding: 16px 24px;
    box-shadow: var(--shadow-sm);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-icon { font-size: 32px; }
.logo h1 { font-size: 24px; font-weight: 600; }

/* 主内容区 */
.main-content {
    display: flex;
    gap: 24px;
    padding: 24px;
    flex: 1;
}

/* 左侧：对话区域 */
.chat-section { flex: 1; min-width: 0; }

.chat-container {
    background: var(--bg-white);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    height: calc(100vh - 140px);
    display: flex;
    flex-direction: column;
}

/* 消息列表 */
.message-list { flex: 1; overflow-y: auto; padding: 24px; }

.message {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.message-avatar {
    width: 40px; height: 40px;
    border-radius: 50%;
    background: var(--bg-primary);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
}

.message-content { flex: 1; min-width: 0; }

.message-text {
    background: var(--bg-primary);
    padding: 12px 16px;
    border-radius: var(--radius-md);
    line-height: 1.6; word-wrap: break-word;
}

.message.assistant .message-text { background: #e6f7ff; }
.message.user { flex-direction: row-reverse; }
.message.user .message-text { background: var(--primary-color); color: white; }

/* 输入区域 */
.input-section { padding: 16px 24px; border-top: 1px solid var(--border-color); }
.input-container { display: flex; gap: 12px; margin-bottom: 12px; }

.user-input {
    flex: 1; padding: 12px 16px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    font-size: 14px; resize: none;
    font-family: inherit; transition: border-color 0.3s;
}

.user-input:focus { outline: none; border-color: var(--primary-color); }

.btn-primary {
    padding: 12px 24px;
    background: var(--primary-color); color: white;
    border: none; border-radius: var(--radius-md);
    font-size: 14px; font-weight: 500;
    cursor: pointer; transition: background 0.3s; white-space: nowrap;
}

.btn-primary:hover { background: var(--primary-hover); }
.btn-primary:disabled { background: var(--border-color); cursor: not-allowed; }

.btn-secondary {
    padding: 8px 16px;
    background: var(--bg-white); color: var(--text-primary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    font-size: 14px; cursor: pointer; transition: all 0.3s;
}

.btn-secondary:hover { color: var(--primary-color); border-color: var(--primary-color); }

.input-hints { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.hint-label { font-size: 12px; color: var(--text-secondary); }

.hint-btn {
    padding: 4px 12px; background: var(--bg-primary);
    border: none; border-radius: 20px;
    font-size: 12px; color: var(--text-secondary);
    cursor: pointer; transition: all 0.3s;
}

.hint-btn:hover { background: var(--primary-color); color: white; }

/* 右侧：推荐结果区域 */
.result-section {
    width: 360px; flex-shrink: 0;
    display: flex; flex-direction: column; gap: 16px;
}

.result-card {
    background: var(--bg-white);
    border-radius: var(--radius-lg);
    padding: 20px;
    box-shadow: var(--shadow-md);
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(20px); }
    to { opacity: 1; transform: translateX(0); }
}

.result-title {
    font-size: 16px; font-weight: 600;
    margin-bottom: 16px;
    display: flex; align-items: center; gap: 8px;
}

.result-icon { font-size: 20px; }

/* 科室卡片 */
.department-card {
    padding: 16px; border: 1px solid var(--border-color);
    border-radius: var(--radius-md); margin-bottom: 12px;
    transition: all 0.3s; cursor: pointer;
}

.department-card:hover { border-color: var(--primary-color); box-shadow: var(--shadow-sm); }

.department-name {
    font-size: 16px; font-weight: 600; margin-bottom: 8px;
    display: flex; justify-content: space-between; align-items: center;
}

.confidence-bar {
    height: 6px; background: var(--bg-primary);
    border-radius: 3px; margin: 8px 0; overflow: hidden;
}

.confidence-fill {
    height: 100%; background: var(--primary-color);
    border-radius: 3px; transition: width 0.5s ease;
}

.department-reason { font-size: 13px; color: var(--text-secondary); line-height: 1.5; }

/* 医生卡片 */
.doctor-card {
    padding: 16px; border: 1px solid var(--border-color);
    border-radius: var(--radius-md); margin-bottom: 12px; transition: all 0.3s;
}

.doctor-header {
    display: flex; justify-content: space-between;
    align-items: start; margin-bottom: 8px;
}

.doctor-name { font-size: 16px; font-weight: 600; }

.doctor-title {
    font-size: 12px; color: var(--primary-color);
    background: #e6f7ff; padding: 2px 8px; border-radius: 10px;
}

.doctor-info { font-size: 13px; color: var(--text-secondary); margin-bottom: 4px; }

.doctor-schedule { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }

.schedule-tag {
    padding: 2px 8px; background: var(--bg-primary);
    border-radius: 10px; font-size: 12px; color: var(--text-secondary);
}

.schedule-tag.available { background: #f6ffed; color: var(--success-color); }

/* 费用卡片 */
.cost-summary {
    display: flex; justify-content: space-between;
    margin-bottom: 16px; padding: 16px;
    background: var(--bg-primary); border-radius: var(--radius-md);
}

.cost-item { text-align: center; }
.cost-label { font-size: 12px; color: var(--text-secondary); margin-bottom: 4px; }
.cost-value { font-size: 20px; font-weight: 600; }
.cost-value.total { color: var(--primary-color); }
.cost-value.insurance { color: var(--success-color); }
.cost-value.self-pay { color: var(--warning-color); }

.cost-breakdown { margin-top: 16px; }

.breakdown-item {
    display: flex; justify-content: space-between;
    padding: 8px 0; border-bottom: 1px solid var(--bg-primary); font-size: 14px;
}

.breakdown-item:last-child { border-bottom: none; }

.insurance-policy {
    margin-top: 16px; padding: 12px;
    background: #fff7e6; border-radius: var(--radius-sm);
    font-size: 13px; color: #d48806; line-height: 1.5;
}

/* 帮助卡片 */
.help-card {
    background: var(--bg-white); border-radius: var(--radius-lg);
    padding: 20px; box-shadow: var(--shadow-md);
}

.help-list { list-style: none; padding: 0; }
.help-list li { padding: 8px 0; font-size: 14px; color: var(--text-secondary); line-height: 1.5; }
.help-list li:before { content: "•"; color: var(--primary-color); font-weight: bold; margin-right: 8px; }

/* 响应式布局 */
@media (max-width: 1024px) {
    .main-content { flex-direction: column; }
    .result-section { width: 100%; }
    .chat-container { height: 60vh; }
}

/* 滚动条样式 */
.message-list::-webkit-scrollbar { width: 6px; }
.message-list::-webkit-scrollbar-track { background: transparent; }
.message-list::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 3px; }
.message-list::-webkit-scrollbar-thumb:hover { background: var(--text-secondary); }

/* 加载动画 */
.loading-dots { display: inline-flex; gap: 4px; }

.loading-dots span {
    width: 8px; height: 8px;
    background: var(--text-secondary);
    border-radius: 50%;
    animation: loading 1.4s ease-in-out infinite;
}

.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes loading {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
    40% { transform: scale(1); opacity: 1; }
}
```

### 6.4 创建工具函数 `frontend/js/utils.js`

```javascript
/**
 * 工具函数模块
 */

/**
 * 格式化时间
 */
function formatTime(date = new Date()) {
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

/**
 * 防抖函数
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * 节流函数
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * 显示/隐藏加载状态
 */
function setLoading(element, isLoading) {
    if (isLoading) {
        element.disabled = true;
        element.querySelector('.btn-text').style.display = 'none';
        element.querySelector('.btn-loading').style.display = 'inline';
    } else {
        element.disabled = false;
        element.querySelector('.btn-text').style.display = 'inline';
        element.querySelector('.btn-loading').style.display = 'none';
    }
}

/**
 * 滚动到元素底部
 */
function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight;
}

/**
 * 创建 DOM 元素
 */
function createElement(tag, attributes = {}, children = []) {
    const element = document.createElement(tag);
    
    // 设置属性
    for (const [key, value] of Object.entries(attributes)) {
        if (key === 'className') {
            element.className = value;
        } else if (key === 'textContent') {
            element.textContent = value;
        } else if (key === 'innerHTML') {
            element.innerHTML = value;
        } else if (key.startsWith('on')) {
            const event = key.toLowerCase().slice(2);
            element.addEventListener(event, value);
        } else {
            element.setAttribute(key, value);
        }
    }
    
    // 添加子元素
    if (Array.isArray(children)) {
        children.forEach(child => {
            if (typeof child === 'string') {
                element.appendChild(document.createTextNode(child));
            } else if (child instanceof HTMLElement) {
                element.appendChild(child);
            }
        });
    } else if (typeof children === 'string') {
        element.textContent = children;
    }
    
    return element;
}

// 导出函数到全局
window.utils = {
    formatTime,
    debounce,
    throttle,
    setLoading,
    scrollToBottom,
    createElement,
};
```

**为什么自己写 `createElement`？** 因为没有用 React/Vue，我们需要一个方便的方式来创建 DOM 元素。这个函数封装了 `document.createElement`，支持设置属性和添加子元素，让代码更简洁。

### 6.5 创建 API 请求封装 `frontend/js/api.js`

```javascript
/**
 * API 请求封装模块
 * 处理所有与后端 API 的通信
 */

// 注意：如果前端由后端静态文件服务（同源），这里设为空字符串
// 如果前端单独运行（不同端口），设为 'http://localhost:8000'
const API_BASE_URL = '';

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

// 导出函数到全局
window.api = {
    recommendDepartment,
    searchDoctors,
    estimateCost,
    sendChatMessage,
};
```

**代码讲解：**

- `fetch()`：浏览器内置的 HTTP 请求函数，用于向服务器发送请求
- `async/await`：异步编程语法，让异步代码看起来像同步代码
- `URLSearchParams`：构建 URL 查询参数的工具，如 `?department=内科&schedule_day=周一`

### 6.6 创建 UI 组件渲染 `frontend/js/components.js`

```javascript
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

// 导出函数到全局
window.components = {
    renderDepartmentCards,
    renderDoctorCards,
    renderCostDetail,
    showResultCard,
    hideResultCard,
};
```

### 6.7 创建对话逻辑 `frontend/js/chat.js`

```javascript
/**
 * 对话逻辑模块
 * 处理用户输入、发送消息、显示响应
 */

// 对话状态
let sessionId = null;
let isProcessing = false;

/**
 * 初始化对话
 */
function initChat() {
    // 生成会话 ID
    sessionId = `session_${Date.now()}`;
    
    // 绑定事件
    bindEvents();
    
    // 显示欢迎消息
    showWelcomeMessage();
}

/**
 * 绑定事件
 */
function bindEvents() {
    const input = document.getElementById('user-input');
    const btnSend = document.getElementById('btn-send');
    const btnClear = document.getElementById('btn-clear');
    
    // 发送按钮点击事件
    btnSend.addEventListener('click', () => sendMessage());
    
    // 输入框回车事件
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // 清空按钮点击事件
    btnClear.addEventListener('click', clearChat);
    
    // 快速输入按钮
    document.querySelectorAll('.hint-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            input.value = btn.dataset.text;
            input.focus();
        });
    });
}

/**
 * 发送消息
 */
async function sendMessage() {
    if (isProcessing) {
        return;
    }
    
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) {
        return;
    }
    
    // 显示用户消息
    appendMessage('user', message);
    
    // 清空输入框
    input.value = '';
    
    // 设置处理状态
    isProcessing = true;
    utils.setLoading(document.getElementById('btn-send'), true);
    
    // 显示加载状态
    appendLoadingMessage();
    
    try {
        // 1. 调用科室推荐 API
        const deptResult = await api.recommendDepartment(message);
        
        // 2. 显示科室推荐结果
        components.renderDepartmentCards(deptResult.departments);
        components.showResultCard('department-result');
        
        // 3. 获取第一个推荐科室，查询医生和费用
        if (deptResult.departments && deptResult.departments.length > 0) {
            const topDept = deptResult.departments[0].name;
            
            // 并行调用医生和费用 API
            const [doctorResult, costResult] = await Promise.all([
                api.searchDoctors(topDept),
                api.estimateCost(topDept),
            ]);
            
            // 显示医生推荐
            if (doctorResult.doctors && doctorResult.doctors.length > 0) {
                components.renderDoctorCards(doctorResult.doctors);
                components.showResultCard('doctor-result');
            }
            
            // 显示费用估算
            components.renderCostDetail(costResult);
            components.showResultCard('cost-result');
        }
        
        // 4. 显示 AI 回复消息
        removeLoadingMessage();
        const replyText = generateReplyText(deptResult);
        appendMessage('assistant', replyText);
        
    } catch (error) {
        console.error('Send Message Error:', error);
        removeLoadingMessage();
        appendMessage('assistant', `抱歉，处理您的请求时出现错误：${error.message}`);
    } finally {
        isProcessing = false;
        utils.setLoading(document.getElementById('btn-send'), false);
    }
}

/**
 * 生成回复文本
 */
function generateReplyText(deptResult) {
    let text = deptResult.reason + '\n\n';
    
    if (deptResult.departments && deptResult.departments.length > 0) {
        text += '推荐科室：\n';
        deptResult.departments.forEach((dept, index) => {
            text += `${index + 1}. ${dept.name} (置信度 ${(dept.confidence * 100).toFixed(0)}%)\n`;
            text += `   ${dept.reason}\n`;
        });
        
        text += '\n我已为您查询了该科室的医生和预估费用，请查看右侧详情。';
    }
    
    return text;
}

/**
 * 显示欢迎消息
 */
function showWelcomeMessage() {
    // 已经在 HTML 中静态定义了欢迎消息
}

/**
 * 添加消息到对话列表
 */
function appendMessage(role, text) {
    const messageList = document.getElementById('message-list');
    
    const messageDiv = utils.createElement('div', {
        className: `message ${role}`,
    }, [
        utils.createElement('div', { className: 'message-avatar' }, [
            role === 'user' ? '👤' : '🤖',
        ]),
        utils.createElement('div', { className: 'message-content' }, [
            utils.createElement('div', { className: 'message-text', textContent: text }),
        ]),
    ]);
    
    messageList.appendChild(messageDiv);
    utils.scrollToBottom(messageList);
}

/**
 * 添加加载状态消息
 */
function appendLoadingMessage() {
    const messageList = document.getElementById('message-list');
    
    const loadingDiv = utils.createElement('div', {
        className: 'message assistant',
        id: 'loading-message',
    }, [
        utils.createElement('div', { className: 'message-avatar' }, ['🤖']),
        utils.createElement('div', { className: 'message-content' }, [
            utils.createElement('div', { className: 'loading-dots' }, [
                utils.createElement('span'),
                utils.createElement('span'),
                utils.createElement('span'),
            ]),
        ]),
    ]);
    
    messageList.appendChild(loadingDiv);
    utils.scrollToBottom(messageList);
}

/**
 * 移除加载状态消息
 */
function removeLoadingMessage() {
    const loadingMessage = document.getElementById('loading-message');
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

/**
 * 清空对话
 */
function clearChat() {
    const messageList = document.getElementById('message-list');
    
    // 保留第一条欢迎消息
    const welcomeMessage = messageList.querySelector('.message');
    messageList.innerHTML = '';
    if (welcomeMessage) {
        messageList.appendChild(welcomeMessage);
    }
    
    // 隐藏结果卡片
    components.hideResultCard('department-result');
    components.hideResultCard('doctor-result');
    components.hideResultCard('cost-result');
    
    // 重新生成会话 ID
    sessionId = `session_${Date.now()}`;
}

/**
 * 初始化（页面加载完成后执行）
 */
document.addEventListener('DOMContentLoaded', initChat);
```

**对话流程讲解：**

```
用户输入 "头痛3天" 并点击发送

    ↓
1. appendMessage('user', '头痛3天')          ← 显示用户消息
    ↓
2. appendLoadingMessage()                    ← 显示加载动画
    ↓
3. api.recommendDepartment('头痛3天')         ← 调用科室推荐API
    ↓
4. renderDepartmentCards(推荐结果)             ← 渲染科室卡片
    ↓
5. Promise.all([                              ← 并行调用
     api.searchDoctors('神经内科'),              ←   医生查询
     api.estimateCost('神经内科')               ←   费用估算
   ])
    ↓
6. renderDoctorCards(医生数据)                  ← 渲染医生卡片
   renderCostDetail(费用数据)                  ← 渲染费用卡片
    ↓
7. removeLoadingMessage()                    ← 移除加载动画
   appendMessage('assistant', 回复文本)        ← 显示AI回复
    ↓
8. 完成！
```

### ✅ 本章验证

前端文件创建完成后，暂时无法单独验证（需要后端运行）。请继续到第 7 章进行联调。

---

## 第 7 章：联调与运行

### 7.1 将前端文件复制到后端静态目录

为了让 FastAPI 直接服务前端页面（这样只需启动一个服务），需要将前端文件复制到 `backend/static/` 目录：

```bash
# 在项目根目录下执行
# Windows:
xcopy /E /I /Y frontend\* backend\static\

# Mac/Linux:
cp -r frontend/* backend/static/
```

> **为什么要复制？** FastAPI 配置了从 `backend/static/` 目录提供静态文件。当浏览器访问 `http://localhost:8000/` 时，FastAPI 会返回 `backend/static/index.html`。这样前端和后端在同一个域名下，不会出现跨域问题。

### 7.2 启动后端服务器

```bash
cd backend

# 确保虚拟环境已激活
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 启动服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7.3 浏览器访问

打开浏览器，访问：

```
http://localhost:8000
```

你应该看到医院智能导诊系统的界面，左侧是对话窗口，右侧是使用提示。

### 7.4 完整测试流程

1. **输入症状**：在输入框中输入"头痛、头晕"
2. **点击发送**（或按回车键）
3. **查看结果**：
   - 左侧对话区显示你的消息和 AI 的回复
   - 右侧依次出现：推荐科室卡片 → 医生推荐卡片 → 费用估算卡片

4. **试试快速输入**：点击下方的"发热咳嗽"、"头痛头晕"等按钮，快速填入症状

5. **清空对话**：点击右上角的"清空"按钮，重置对话

### 7.5 常见问题排查

#### 问题 1：端口被占用

**现象**：启动时提示 `Address already in use`

**解决**：

```bash
# Windows: 查找并杀掉占用 8000 端口的进程
netstat -ano | findstr :8000
taskkill /F /PID <进程ID>

# Mac/Linux:
lsof -i :8000
kill -9 <进程ID>

# 或者换个端口启动
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

#### 问题 2：API 请求失败（跨域错误）

**现象**：浏览器控制台显示 `CORS error`

**解决**：确保 `main.py` 中的 CORS 配置正确：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_methods=["*"],
    allow_headers=["*"],
)
```

如果前端由后端静态文件服务（同源），则不会有跨域问题。如果前端单独运行（如用 `python -m http.server`），确保 CORS 已配置。

#### 问题 3：中文显示乱码

**现象**：API 返回的中文显示为乱码

**解决**：确保所有 JSON 文件以 UTF-8 编码保存。在 VS Code 中，点击右下角的编码，选择"UTF-8"。

#### 问题 4：前端页面空白

**现象**：访问 `http://localhost:8000` 显示空白页面

**解决**：
1. 检查 `backend/static/index.html` 是否存在
2. 打开浏览器开发者工具（F12），查看 Console 是否有错误
3. 检查 JS 文件路径是否正确（`js/utils.js` 而不是 `/js/utils.js`）

### ✅ 本章验证

1. 浏览器访问 `http://localhost:8000` 能看到系统界面
2. 输入症状后，右侧能显示推荐结果
3. 点击"清空"能重置对话

---

## 第 8 章：Docker 部署（可选）

> Docker 可以让你把整个系统打包成容器，在任何安装了 Docker 的机器上运行，不需要手动安装 Python 和依赖。这一章是可选的，如果你只想本地运行，可以跳过。

### 8.1 前提条件

安装 Docker 和 Docker Compose：
- Docker：https://docs.docker.com/get-docker/
- Docker Compose：通常随 Docker 一起安装

### 8.2 后端 Dockerfile

创建文件 `backend/Dockerfile`：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖（gcc 编译器，部分 Python 包编译需要）
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装 Python 包（使用清华镜像加速）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Dockerfile 讲解：**

| 指令 | 作用 |
|------|------|
| `FROM python:3.10-slim` | 基于 Python 3.10 精简版镜像 |
| `WORKDIR /app` | 设置工作目录 |
| `RUN apt-get install gcc` | 安装 C 编译器（部分 Python 包需要） |
| `COPY requirements.txt .` | 复制依赖文件 |
| `RUN pip install` | 安装 Python 依赖 |
| `COPY . .` | 复制所有代码 |
| `EXPOSE 8000` | 声明容器监听 8000 端口 |
| `CMD` | 容器启动命令 |

### 8.3 前端 Dockerfile

创建文件 `frontend/Dockerfile`：

```dockerfile
FROM nginx:alpine

# 复制前端文件到 Nginx 静态文件目录
COPY . /usr/share/nginx/html

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
```

### 8.4 Nginx 配置

创建文件 `frontend/nginx.conf`：

```nginx
server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    # SPA 路由回退（支持前端路由）
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 如果需要代理后端 API（取消注释即可启用）
    # location /api/ {
    #     proxy_pass http://backend:8000;
    #     proxy_set_header Host $host;
    #     proxy_set_header X-Real-IP $remote_addr;
    # }
}
```

### 8.5 Docker Compose 编排

创建文件 `docker-compose.yml`（在项目根目录）：

```yaml
version: '3.8'

services:
  # Milvus 依赖：etcd（存储元数据）
  milvus-etcd:
    container_name: milvus-etcd
    image: quay.io/coreos/etcd:v3.5.18
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/etcd:/etcd
    command: >-
      etcd -advertise-client-urls=http://127.0.0.1:2379
      -listen-client-urls http://0.0.0.0:2379
      -data-dir /etcd
    healthcheck:
      test: ["CMD", "etcdctl", "endpoint", "health"]
      interval: 30s
      timeout: 20s
      retries: 3

  # Milvus 依赖：MinIO（存储向量数据）
  milvus-minio:
    container_name: milvus-minio
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/minio:/minio_data
    command: minio server /minio_data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  # Milvus 向量数据库主服务（后续 RAG 进阶用）
  milvus-standalone:
    container_name: milvus-standalone
    image: milvusdb/milvus:v2.4.17
    command: ["milvus", "run", "standalone"]
    environment:
      - ETCD_ENDPOINTS=milvus-etcd:2379
      - MINIO_ADDRESS=milvus-minio:9000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      milvus-etcd:
        condition: service_healthy
      milvus-minio:
        condition: service_healthy

  # 后端 FastAPI 服务
  backend:
    container_name: guidancesystem-backend
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "${BACKEND_PORT:-8000}:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY:-}
      - OPENAI_BASE_URL=${OPENAI_BASE_URL:-https://api.openai.com/v1}
      - MILVUS_HOST=milvus-standalone
      - MILVUS_PORT=19530
    volumes:
      - ./backend:/app
    depends_on:
      - milvus-standalone
    restart: unless-stopped

  # 前端 Nginx 静态文件服务
  frontend:
    container_name: guidancesystem-frontend
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "${FRONTEND_PORT:-8080}:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  etcd:
  minio:
  milvus:
```

### 8.6 环境变量配置

创建文件 `.env.example`：

```env
# 医院智能导诊系统 - 环境变量配置

# OpenAI API Key（可选，如果没有配置，系统将使用规则引擎）
# OPENAI_API_KEY=sk-your-openai-api-key-here

# API 基础 URL（如果使用兼容接口，如 DeepSeek、通义千问等）
# OPENAI_API_BASE=https://api.openai.com/v1

# 向量数据库配置（可选，如果不用 Milvus，系统将使用简单向量检索）
# MILVUS_HOST=localhost
# MILVUS_PORT=19530

# 嵌入模型配置
# EMBEDDING_MODEL=text-embedding-3-small

# 是否使用 Mock 模式（true = 不使用真实 LLM，使用规则引擎）
USE_MOCK=true
```

### 8.7 Docker 启动命令

```bash
# 复制环境变量模板
cp .env.example .env

# 启动所有服务（首次会下载镜像，需要等待）
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看后端日志
docker-compose logs -f backend

# 停止所有服务
docker-compose down

# 如果只需要后端和前端（不启动 Milvus）
docker-compose up -d backend frontend
```

### ✅ 本章验证

1. `docker-compose ps` 显示所有服务状态为 `running`
2. 访问 `http://localhost:8080` 能看到前端页面
3. 访问 `http://localhost:8000/docs` 能看到 API 文档

---

## 第 9 章：进阶指引

### 9.1 当前系统 vs 目标系统

| 功能 | 当前状态 | 目标状态 |
|------|---------|---------|
| 科室推荐 | ✅ 规则引擎（关键词匹配） | LLM 语义理解 |
| 医生查询 | ✅ JSON 数据查询 | 数据库查询 |
| 费用估算 | ✅ JSON 数据计算 | 实时价格查询 |
| 对话管理 | ✅ 内存会话 | 数据库持久化 |
| 知识检索 | ❌ 未实现 | RAG 向量检索 |
| 智能推理 | ❌ 未实现 | ReAct Agent |
| 多链路推理 | ❌ 未实现 | 三链并行 CoT |

### 9.2 接入 OpenAI API

如果你想让系统更智能（用 LLM 理解症状），可以接入 OpenAI API：

**步骤 1：安装依赖**

```bash
pip install openai langchain langchain-openai
```

**步骤 2：配置环境变量**

在 `.env` 文件中设置：

```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
# 如果用国内兼容接口（如 DeepSeek）：
# OPENAI_API_BASE=https://api.deepseek.com/v1
```

**步骤 3：创建 LLM 服务 `app/rag/llm.py`**

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
)

def chat_with_llm(prompt: str, system_prompt: str = "") -> str:
    """调用 LLM 生成回复"""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content
```

**步骤 4：在科室推荐中接入 LLM**

修改 `app/api/department.py` 中的推荐逻辑，用 LLM 分析症状：

```python
from app.rag.llm import chat_with_llm

async def recommend_with_llm(symptoms: str) -> dict:
    """使用 LLM 分析症状并推荐科室"""
    prompt = f"""
    患者描述的症状：{symptoms}
    
    请分析症状，推荐最合适的科室，返回 JSON 格式：
    {{
        "departments": [
            {{"name": "科室名", "confidence": 0.9, "reason": "推荐理由"}}
        ]
    }}
    """
    response = chat_with_llm(prompt)
    import json
    return json.loads(response)
```

### 9.3 实现 RAG 检索

> **什么是 RAG？** RAG（Retrieval-Augmented Generation）是"检索增强生成"。先从知识库中检索相关文档，然后把检索到的内容作为上下文传给 LLM，让 LLM 基于这些知识生成回答。

**架构：**

```
用户提问 → 向量化 → Milvus 检索 → 取回相关文档 → 拼接 Prompt → LLM 生成回答
```

**实现步骤：**

1. 启动 Milvus（用 Docker Compose）
2. 将医疗知识文档（`medical_knowledge/` 目录下的 MD 文件）向量化并存入 Milvus
3. 用户提问时，先检索相关文档，再传给 LLM

### 9.4 实现 ReAct Agent

> **什么是 ReAct？** ReAct = Reasoning + Acting。让 AI 先"思考"（Thought），再决定"行动"（Action），然后"观察"结果（Observation），循环直到得出最终答案。

**示例流程：**

```
用户："我头痛3天了"

Thought 1: 用户描述了头痛症状，需要推荐科室
Action 1: 调用 search_department("头痛")
Observation 1: 推荐神经内科，置信度 90%

Thought 2: 需要查询神经内科的医生
Action 2: 调用 search_doctor("神经内科")
Observation 2: 找到张明华医生，周一上午出诊

Thought 3: 需要估算费用
Action 3: 调用 estimate_cost("神经内科")
Observation 3: 总费用 520 元，医保支付 411 元

Thought 4: 信息齐全，生成最终回答
Final Answer: 根据您的症状，推荐神经内科...
```

### 9.5 架构升级路线图

```
当前（规则引擎版）          →    进阶（LLM 版）           →    完整版（RAG + ReAct）
─────────────────         ──────────────────         ──────────────────────────
✅ 关键词匹配科室            LLM 语义理解症状              RAG 检索医疗知识库
✅ JSON 数据查询医生          LLM 生成推荐理由             ReAct Agent 自主决策
✅ JSON 数据计算费用          LLM 解释费用明细             多链路并行 CoT 推理
✅ 内存会话管理              数据库持久化                 LangGraph 状态机
                          SSE 流式 LLM 输出            用户认证 + 历史记录
```

---

## 附录

### A. 完整项目目录树

```
hospital-guide-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI 主入口
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py             # 对话管理 API
│   │   │   ├── cost.py             # 费用估算 API
│   │   │   ├── department.py       # 科室推荐 API
│   │   │   └── doctor.py            # 医生查询 API
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py             # 聊天数据模型
│   │   │   └── response.py          # 响应数据模型
│   │   └── data/
│   │       ├── cost_insurance.json  # 费用医保数据
│   │       ├── departments.json     # 科室数据
│   │       ├── doctors.json         # 医生数据
│   │       └── symptom_disease.json # 症状-疾病映射
│   ├── static/                     # 前端文件副本
│   │   ├── index.html
│   │   ├── css/style.css
│   │   └── js/
│   │       ├── api.js
│   │       ├── chat.js
│   │       ├── components.js
│   │       └── utils.js
│   ├── Dockerfile
│   ├── requirements.txt
│   └── venv/                       # 虚拟环境
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   ├── js/
│   │   ├── api.js
│   │   ├── chat.js
│   │   ├── components.js
│   │   └── utils.js
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── .env.example
├── start.bat                        # Windows 启动脚本
└── start.sh                         # Mac/Linux 启动脚本
```

### B. API 接口速查表

| 接口 | 方法 | 路径 | 参数 | 说明 |
|------|------|------|------|------|
| 创建会话 | POST | `/api/v1/chat/session` | 无 | 返回 session_id |
| 发送消息 | POST | `/api/v1/chat/send` | body: `{session_id, message}` | 返回 AI 回复 + 科室推荐 |
| 流式消息 | GET | `/api/v1/chat/stream` | query: `session_id, message` | SSE 流式响应 |
| 科室推荐 | POST | `/api/v1/department/recommend` | body: `{symptoms}` | 返回推荐科室列表 |
| 医生查询 | GET | `/api/v1/doctors` | query: `department, schedule_day?` | 返回医生列表 |
| 费用估算 | POST | `/api/v1/cost/estimate` | body: `{department}` | 返回费用明细 |
| API 文档 | GET | `/docs` | 无 | Swagger UI |

### C. 常见错误与解决方案（FAQ）

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `ModuleNotFoundError: No module named 'fastapi'` | 虚拟环境未激活 | 运行 `venv\Scripts\activate` |
| `Address already in use` | 端口被占用 | 换端口或杀掉占用进程 |
| `CORS error` | 跨域未配置 | 检查 main.py 中 CORS 中间件 |
| `FileNotFoundError: departments.json` | 路径错误 | 确认数据文件在 `app/data/` 目录 |
| `JSON parse error` | 请求体格式错误 | 检查 Content-Type 是否为 application/json |
| 中文乱码 | 编码问题 | 确保文件以 UTF-8 编码保存 |

### D. 推荐学习资源

| 主题 | 资源 |
|------|------|
| FastAPI 官方文档 | https://fastapi.tiangolo.com/zh/ |
| Pydantic 文档 | https://docs.pydantic.dev/ |
| Python JSON 处理 | https://docs.python.org/3/library/json.html |
| HTML/CSS/JS 基础 | https://developer.mozilla.org/zh-CN/docs/Web |
| fetch API | https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API |
| Docker 入门 | https://docs.docker.com/get-started/ |
| LangChain 文档 | https://python.langchain.com/ |
| Milvus 文档 | https://milvus.io/docs |

---

> 🎉 **恭喜！** 你已经完成了医院智能导诊系统的搭建。现在你拥有一个可以运行的完整项目，包含后端 API、前端界面、示例数据和 Docker 部署方案。
>
> 接下来你可以：
> 1. 尝试接入 OpenAI API，让系统更智能
> 2. 添加更多科室、医生和症状数据
> 3. 实现用户登录和历史记录功能
> 4. 部署到云服务器，让其他人也能访问
>
> 有问题随时查阅本教程的 FAQ 部分，或参考推荐学习资源继续深入学习。祝学习愉快！
