# 医院智能导诊系统 — PyCharm 实操搭建教程

> 本教程以 PyCharm 为开发工具，按照真实项目开发流程，手把手教你从零搭建一个完整的医院智能导诊问答系统。每一步都配有 PyCharm 操作截图说明，跟着做就能跑起来。

---

## 目录

- [第 0 章：开发前准备](#第-0-章开发前准备)
- [第 1 章：创建 PyCharm 项目](#第-1-章创建-pycharm-项目)
- [第 2 章：配置 Python 解释器与虚拟环境](#第-2-章配置-python-解释器与虚拟环境)
- [第 3 章：搭建项目骨架](#第-3-章搭建项目骨架)
- [第 4 章：编写后端代码（核心）](#第-4-章编写后端代码核心)
- [第 5 章：运行与调试后端](#第-5-章运行与调试后端)
- [第 6 章：API 接口测试](#第-6-章api-接口测试)
- [第 7 章：编写前端代码](#第-7-章编写前端代码)
- [第 8 章：前后端联调](#第-8-章前后端联调)
- [第 9 章：Docker 部署（可选）](#第-9-章docker-部署可选)
- [附录 A：PyCharm 常用快捷键](#附录-a-pycharm-常用快捷键)
- [附录 B：常见问题排查](#附录-b-常见问题排查)

---

## 第 0 章：开发前准备

### 0.1 项目简介

我们要搭建的是一个**医院智能导诊问答系统**。用户在网页上输入症状（如"头痛、恶心"），系统返回：

1. **推荐科室** — 基于症状推断可能的疾病，匹配对应科室
2. **医生信息** — 展示该科室的医生、职称、排班
3. **费用估算** — 常见检查项目费用与医保报销金额

最终效果：浏览器打开 → 输入症状 → 右侧自动弹出科室/医生/费用卡片。

### 0.2 技术栈

| 层面 | 技术 | 说明 |
|------|------|------|
| IDE | PyCharm（Community 或 Professional 均可） | 主开发工具 |
| 后端 | FastAPI + Python 3.10+ | API 框架 |
| 数据 | JSON 文件 | 轻量数据存储 |
| 前端 | 纯 HTML + CSS + JavaScript | 无需构建工具 |
| 部署 | Docker Compose（可选） | 容器化部署 |

### 0.3 开发流程总览

```
需求理解 → 环境准备 → 创建项目 → 搭建骨架
    → 编写后端代码 → 运行调试 → 接口测试
    → 编写前端代码 → 前后端联调 → 部署上线
```

### 0.4 你需要提前安装的东西

#### 1. Python 3.10+

- 下载地址：https://www.python.org/downloads/
- 安装时**务必勾选 "Add Python to PATH"**
- 验证：打开 CMD/Terminal，输入 `python --version`，应显示 `Python 3.10.x` 或更高

#### 2. PyCharm

- 下载地址：https://www.jetbrains.com/pycharm/download/
- **Community 版免费**，对本项目完全够用
- Professional 版有更多功能（数据库工具、前端开发等），但非必须
- 安装过程一路 Next 即可

#### 3. Docker（可选，仅第 9 章需要）

- 下载地址：https://docs.docker.com/get-docker/
- 如果不学 Docker 部署章节，可以不装

### ✅ 本章检查清单

- [ ] Python 3.10+ 已安装，`python --version` 能正常输出版本号
- [ ] PyCharm 已安装
- [ ] （可选）Docker 已安装

---

## 第 1 章：创建 PyCharm 项目

### 1.1 启动 PyCharm

首次打开 PyCharm，会弹出欢迎界面：

```
┌──────────────────────────────────────┐
│         Welcome to PyCharm           │
│                                      │
│   + New Project                      │
│   📁 Open                            │
│   📂 Get from VCS                    │
│                                      │
│   Recent Projects:                   │
│   (空)                                │
└──────────────────────────────────────┘
```

点击 **「New Project」**。

### 1.2 配置新项目

在弹出的「New Project」窗口中，填写以下信息：

```
┌──────────────────────────────────────────────────────┐
│  New Project                                          │
│                                                       │
│  Location: C:\Users\你的用户名\PycharmProjects\hospital-guide  │
│                                                       │
│  Python Interpreter:                                  │
│  ○ New environment using:  [Virtualenv ▼]            │
│      Base interpreter: [Python 3.10 ▼]               │
│      Location: ...\hospital-guide\venv                │
│                                                       │
│  ○ Previously configured interpreter:                │
│      [Python 3.10 ▼]                                 │
│                                                       │
│  ☑ Create main.py welcome script                     │
│                                                       │
│              [Create]                                │
└──────────────────────────────────────────────────────┘
```

**操作步骤：**

1. **Location**：选择项目存放路径，建议放在 `PycharmProjects` 目录下，项目名设为 `hospital-guide`
2. **Python Interpreter**：选择 **「New environment using Virtualenv」**（让 PyCharm 自动创建虚拟环境）
3. **Base interpreter**：选择你安装的 Python 3.10
4. **取消勾选**「Create main.py welcome script」（我们不需要自动生成的模板文件）
5. 点击 **「Create」**

### 1.3 等待项目初始化

PyCharm 会自动：
- 创建项目目录
- 创建虚拟环境（venv）
- 建立项目索引

初始化完成后，你会看到 PyCharm 主界面：

```
┌──────────┬─────────────────────────────────────┐
│  Project  │  hospital-guide                     │
│  工具栏    │                                     │
│           │  # 这是一个空项目                     │
│  ▸ venv/  │                                     │
│           │                                     │
│  .idea/   │                                     │
│           │                                     │
└──────────┴─────────────────────────────────────┘
     左侧           中间编辑区
```

### 1.4 认识 PyCharm 界面

| 区域 | 名称 | 作用 |
|------|------|------|
| 左侧 | Project 视图 | 文件目录树，双击文件打开编辑 |
| 中间 | 编辑区 | 写代码的地方 |
| 底部 | Terminal（终端） | 内置命令行，可运行命令 |
| 底部 | Python Console | 交互式 Python 环境 |
| 底部 | Run/Debug | 运行输出和调试信息 |
| 右侧 | TODO | 待办事项（自动扫描代码中的注释） |

> **提示**：如果左侧 Project 视图没显示，点击菜单 `View → Tool Windows → Project`，或按快捷键 `Alt+1`。

### ✅ 本章验证

- [ ] PyCharm 已打开新项目
- [ ] 左侧能看到 `venv/` 和 `.idea/` 目录
- [ ] 底部能找到 Terminal 标签

---

## 第 2 章：配置 Python 解释器与虚拟环境

### 2.1 确认虚拟环境已创建

在第 1 章创建项目时，PyCharm 会自动创建虚拟环境。确认方法：

**方法 1：查看左侧文件树**

左侧 Project 视图应该有 `venv/` 文件夹。展开它，能看到 `Scripts/`（Windows）或 `bin/`（Mac）目录。

**方法 2：查看右下角状态栏**

PyCharm 右下角会显示当前使用的 Python 解释器：

```
hospital-guide | Python 3.10 (hospital-guide) | UTF-8 | LF
                    ↑
           括号里是虚拟环境名称
```

**方法 3：用终端验证**

点击底部 **Terminal** 标签，输入：

```bash
# Windows:
where python
# 应显示 ...\venv\Scripts\python.exe

# Mac/Linux:
which python
# 应显示 .../venv/bin/python
```

如果命令行前面有 `(venv)` 前缀，说明虚拟环境已激活。

### 2.2 手动配置解释器（如果没自动配置）

如果右下角显示的不是虚拟环境的 Python，或你选择了「Previously configured interpreter」，需要手动配置：

1. 点击菜单 **`File → Settings`**（Mac：`PyCharm → Preferences`）
2. 左侧导航：**`Project: hospital-guide → Python Interpreter`**

```
┌──────────────────────────────────────────────┐
│  Settings                                     │
│                                               │
│  Project: hospital-guide                      │
│  ├─ Python Interpreter                       │
│                                               │
│  ┌─────────────────────────────────────────┐  │
│  │  Python Interpreter:                    │  │
│  │  Python 3.10 (hospital-guide) ▼        │  │
│  │                                          │  │
│  │  [+] [-] [⏻]                           │  │
│  │                                          │  │
│  │  Name          Version    Latest        │  │
│  │  (空 — 还没安装任何包)                    │  │
│  └─────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

3. 点击右侧齿轮 ⚙️ → **`Add...`**
4. 选择 **`Add Interpreter → Add Local Interpreter`**
5. 选择 **`Virtualenv Environment → New`**
6. Base interpreter 选择 Python 3.10
7. 点击 **OK**，等待创建完成

### 2.3 在 PyCharm 终端安装依赖

点击底部 **Terminal** 标签，执行以下命令安装 FastAPI 等依赖：

```bash
# 先创建 requirements.txt 文件（下一章会在 PyCharm 中创建）
# 这里先直接安装核心依赖

pip install fastapi uvicorn[standard] pydantic python-dotenv requests
```

> **提示**：如果下载速度慢，使用国内镜像：
> ```bash
> pip install fastapi uvicorn[standard] pydantic -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

安装完成后，验证：

```bash
python -c "import fastapi; print(f'FastAPI {fastapi.__version__} 安装成功')"
```

### 2.4 配置 PyCharm 的包管理（可选）

PyCharm 也可以用图形界面安装包：

1. 打开 `Settings → Project → Python Interpreter`
2. 点击 **`+`** 按钮
3. 搜索包名（如 `fastapi`）
4. 点击 **`Install Package`**

```
┌──────────────────────────────────────────────┐
│  Available Packages                          │
│                                               │
│  Search: [fastapi              ]              │
│                                               │
│  ┌─────────────────────────────────────────┐  │
│  │  fastapi                                 │  │
│  │  FastAPI framework, high performance...  │  │
│  │  Latest version: 0.115.0                 │  │
│  │  Released: ...                           │  │
│  └─────────────────────────────────────────┘  │
│                                               │
│  [Install Package]                            │
└──────────────────────────────────────────────┘
```

> **建议**：日常开发用终端 `pip install` 更快，需要查看包文档时用 PyCharm 图形界面。

### ✅ 本章验证

- [ ] 右下角显示 `Python 3.10 (hospital-guide)`
- [ ] 终端执行 `python -c "import fastapi"` 无报错
- [ ] `Settings → Python Interpreter` 中能看到已安装的包

---

## 第 3 章：搭建项目骨架

### 3.1 在 PyCharm 中创建目录

在左侧 **Project 视图**中，右键点击项目根目录 `hospital-guide` → **`New → Directory`**：

按照以下顺序创建目录（每创建一个，右键再创建下一个）：

```
hospital-guide/
├── backend/              ← 右键项目根 → New → Directory → 输入 backend
│   ├── app/              ← 右键 backend → New → Directory → 输入 app
│   │   ├── api/          ← 右键 app → New → Directory → 输入 api
│   │   ├── models/       ← 右键 app → New → Directory → 输入 models
│   │   └── data/         ← 右键 app → New → Directory → 输入 data
│   └── static/           ← 右键 backend → New → Directory → 输入 static
└── frontend/             ← 右键项目根 → New → Directory → 输入 frontend
    ├── css/              ← 右键 frontend → New → Directory → 输入 css
    └── js/               ← 右键 frontend → New → Directory → 输入 js
```

### 3.2 创建 Python 包标识文件 `__init__.py`

> **什么是 `__init__.py`？** 在 Python 中，包含 `__init__.py` 文件的目录才能被 `import` 语句导入。这个文件告诉 Python"这个目录是一个包"。

创建方法：右键点击目录 → **`New → Python Package`**（这会自动创建 `__init__.py`）

或者手动创建：右键目录 → **`New → File`** → 输入 `__init__.py`（文件内容留空）

需要创建 `__init__.py` 的目录：

```
backend/app/__init__.py
backend/app/api/__init__.py
backend/app/models/__init__.py
```

### 3.3 创建 requirements.txt

右键点击 `backend` 目录 → **`New → File`** → 输入 `requirements.txt`

输入以下内容：

```txt
# FastAPI 框架
fastapi>=0.115.0
uvicorn[standard]>=0.34.0

# 数据处理
pydantic>=2.10.0
python-dotenv>=1.0.0

# HTTP 请求（测试用）
requests>=2.32.0

# 以下为进阶功能依赖（基础版可暂时不装）
# langchain>=0.3.0
# langchain-openai>=0.2.0
# pymilvus>=2.5.0
# openai>=1.60.0
# scikit-learn>=1.6.0
# numpy>=2.1.0
```

### 3.4 在 PyCharm 终端安装依赖

如果之前没装，现在在 **Terminal** 中执行：

```bash
cd backend
pip install -r requirements.txt
```

### 3.5 最终项目骨架

创建完所有目录和文件后，左侧 Project 视图应该是：

```
hospital-guide/
├── .idea/                    ← PyCharm 配置（自动生成）
├── venv/                     ← 虚拟环境（自动生成）
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   └── __init__.py
│   │   └── data/
│   ├── static/
│   └── requirements.txt
└── frontend/
    ├── css/
    └── js/
```

### ✅ 本章验证

- [ ] 左侧目录树与上图结构一致
- [ ] `backend/app/__init__.py` 等文件存在
- [ ] `backend/requirements.txt` 存在且依赖已安装

---

## 第 4 章：编写后端代码（核心）

> **开发顺序**：数据 → 模型 → API → 主入口。这是标准的"自底向上"开发流程：先准备数据，再定义数据结构，然后写业务逻辑，最后组装入口。

### 4.1 编写数据文件（JSON）

#### 步骤：在 PyCharm 中创建 JSON 文件

1. 右键点击 `backend/app/data` 目录
2. 选择 **`New → File`**
3. 输入文件名（如 `departments.json`）
4. 在编辑区输入内容
5. `Ctrl+S`（Mac：`Cmd+S`）保存

#### 4.1.1 科室数据 `departments.json`

右键 `data` → New → File → 输入 `departments.json`：

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

> **PyCharm 提示**：PyCharm 会自动检测 JSON 语法。如果有格式错误，行号旁会出现红色波浪线。`Ctrl+Alt+L`（Mac：`Cmd+Alt+L`）可以自动格式化 JSON。

#### 4.1.2 医生数据 `doctors.json`

同样方法创建，内容如下：

```json
[
  {
    "id": "doc_001",
    "name": "张明华",
    "department": "神经内科",
    "title": "主任医师",
    "specialty": "偏头痛、癫痫、帕金森病",
    "schedule": {"周一": "上午", "周三": "全天", "周五": "上午"},
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
    "schedule": {"周二": "全天", "周四": "上午", "周六": "上午"},
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
    "schedule": {"周一": "全天", "周三": "上午", "周四": "全天"},
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
    "schedule": {"周二": "上午", "周五": "全天"},
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
    "schedule": {"周一": "上午", "周三": "全天", "周五": "上午"},
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
    "schedule": {"周二": "全天", "周四": "全天", "周六": "上午"},
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
    "schedule": {"周一": "全天", "周三": "上午", "周五": "全天"},
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
    "schedule": {"周二": "全天", "周四": "上午", "周五": "上午"},
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
    "schedule": {"周一": "全天", "周三": "全天", "周五": "上午"},
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
    "schedule": {"周二": "全天", "周四": "全天"},
    "rating": 4.8,
    "experience_years": 23,
    "introduction": "眼科专家，擅长白内障超声乳化手术和青光眼手术。"
  }
]
```

#### 4.1.3 症状-疾病映射 `symptom_disease.json`

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

> **这个文件是科室推荐算法的核心**：`症状 → [可能的疾病列表]`。用户输入"头痛"，系统查到头痛可能对应 5 种疾病，再去找哪些科室能治这些病。

#### 4.1.4 费用医保数据 `cost_insurance.json`

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

### 4.2 编写数据模型

#### PyCharm 操作

1. 右键 `backend/app/models` → **`New → Python File`**
2. 输入文件名 `chat.py`
3. 在编辑区输入代码
4. `Ctrl+S` 保存

#### 4.2.1 `models/chat.py`

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

> **PyCharm 提示**：输入 `from pydantic import` 时，PyCharm 会自动补全。如果出现红色波浪线（找不到 pydantic），说明虚拟环境未正确配置，回到第 2 章检查。

#### 4.2.2 `models/response.py`

同样方法创建：

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

### 4.3 编写 API 端点

#### PyCharm 操作

右键 `backend/app/api` → **`New → Python File`** → 依次创建 4 个文件

#### 4.3.1 `api/department.py` — 科室推荐

```python
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import json
import os

from app.models.response import DepartmentRecommendRequest, DepartmentRecommendResponse

router = APIRouter()


def load_departments():
    """加载科室数据"""
    data_path = os.path.join(os.path.dirname(__file__), "../data/departments.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


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
        departments = load_departments()
        symptom_disease_map = load_symptom_disease()

        # 步骤1：提取症状关键词
        symptoms = []
        for symptom in symptom_disease_map.keys():
            if symptom in request.symptoms:
                symptoms.append(symptom)

        # 步骤2：如果没有精确匹配，尝试分词
        if not symptoms:
            import re
            words = re.split(r'[,，、\s]+', request.symptoms)
            for word in words:
                word = word.strip()
                if word and word in symptom_disease_map:
                    symptoms.append(word)

        if not symptoms:
            return DepartmentRecommendResponse(
                departments=[{
                    "name": dept["name"],
                    "confidence": 0.5,
                    "reason": "未识别到具体症状，请详细描述您的症状"
                } for dept in departments[:3]]
            )

        # 步骤3：统计疾病出现次数
        disease_count = {}
        for symptom in symptoms:
            if symptom in symptom_disease_map:
                for disease in symptom_disease_map[symptom]:
                    disease_count[disease] = disease_count.get(disease, 0) + 1

        # 步骤4：根据疾病匹配科室
        dept_score = {}
        for disease, count in disease_count.items():
            for dept in departments:
                if disease in dept.get("common_diseases", []):
                    if dept["name"] not in dept_score:
                        dept_score[dept["name"]] = {"score": 0, "diseases": []}
                    dept_score[dept["name"]]["score"] += count
                    dept_score[dept["name"]]["diseases"].append(disease)

        # 步骤5：计算置信度并排序
        results = []
        for dept_name, info in dept_score.items():
            confidence = min(0.95, 0.6 + info["score"] * 0.1)
            results.append({
                "name": dept_name,
                "confidence": round(confidence, 2),
                "reason": f"根据您描述的症状，可能患有{'、'.join(info['diseases'][:3])}等疾病，建议就诊{dept_name}"
            })

        if not results:
            results.append({
                "name": "神经内科",
                "confidence": 0.6,
                "reason": "根据常见症状，建议先到神经内科就诊"
            })

        results.sort(key=lambda x: x["confidence"], reverse=True)

        return DepartmentRecommendResponse(
            departments=results[:3],
            reason=f"根据您描述的症状（{','.join(symptoms)}），为您推荐以下科室"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"科室推荐失败: {str(e)}")
```

> **算法核心**：用户输入"头痛" → 查 symptom_disease.json 得到["偏头痛","高血压",...] → 查 departments.json 找哪些科室的 common_diseases 包含这些疾病 → 匹配到神经内科和心血管内科 → 计算置信度排序。

#### 4.3.2 `api/doctor.py` — 医生查询

```python
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import json
import os

from app.models.response import DoctorQueryResponse

router = APIRouter()


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
    """查询医生"""
    try:
        doctors = load_doctors()

        # 精确匹配科室
        filtered = [doc for doc in doctors if doc["department"] == department]

        # 模糊匹配
        if not filtered:
            for doc in doctors:
                if department in doc["department"] or doc["department"] in department:
                    filtered.append(doc)

        # 按排班日过滤
        if schedule_day:
            filtered = [doc for doc in filtered if schedule_day in doc.get("schedule", {})]

        # 按评分排序
        filtered.sort(key=lambda x: x.get("rating", 0), reverse=True)

        return DoctorQueryResponse(doctors=filtered)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询医生失败: {str(e)}")
```

#### 4.3.3 `api/cost.py` — 费用估算

```python
from fastapi import APIRouter, HTTPException
import json
import os

from app.models.response import CostEstimateRequest, CostEstimateResponse

router = APIRouter()


def load_cost_insurance():
    """加载费用医保数据"""
    data_path = os.path.join(os.path.dirname(__file__), "../data/cost_insurance.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


@router.post("/estimate", response_model=CostEstimateResponse)
async def estimate_cost(request: CostEstimateRequest):
    """估算费用"""
    try:
        data = load_cost_insurance()
        dept_data = data.get("departments", {}).get(request.department)

        if not dept_data:
            return CostEstimateResponse(
                total=300, insurance_pay=210, self_pay=90,
                breakdown=[{"name": "挂号费", "price": 50, "insurance_rate": 0.8}],
                insurance_policy=data.get("insurance_policy", {}).get("description")
            )

        breakdown = dept_data.get("common_procedures", [])
        total = sum(item["price"] for item in breakdown)
        insurance_pay = sum(item["price"] * item.get("insurance_rate", 0.7) for item in breakdown)
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

#### 4.3.4 `api/chat.py` — 对话管理

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import Dict, Any
import json
import asyncio
import uuid

from app.models.chat import ChatRequest, SessionResponse
from app.api.department import load_departments, load_symptom_disease

router = APIRouter()

# 内存会话存储（重启即丢失，生产环境应使用数据库）
sessions: Dict[str, Dict[str, Any]] = {}


@router.post("/session", response_model=SessionResponse)
async def create_session():
    """创建新会话"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"messages": [], "created_at": asyncio.get_event_loop().time()}
    return SessionResponse(session_id=session_id)


@router.post("/send")
async def send_message(request: ChatRequest):
    """发送消息（非流式）"""
    try:
        session = sessions.get(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")

        session["messages"].append({"role": "user", "content": request.message})

        departments = analyze_symptoms(request.message)
        ai_response = generate_response(request.message, departments)

        ai_message = {"role": "assistant", "content": ai_response}
        session["messages"].append(ai_message)

        return {"session_id": request.session_id, "message": ai_message, "departments": departments}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"发送消息失败: {str(e)}")


@router.get("/stream")
async def stream_message(session_id: str, message: str):
    """发送消息（SSE 流式响应，逐字输出）"""
    try:
        session = sessions.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")

        session["messages"].append({"role": "user", "content": message})
        departments = analyze_symptoms(message)
        ai_response = generate_response(message, departments)

        async def generate_sse():
            yield f"data: {json.dumps({'type': 'start'})}\n\n"
            for char in ai_response:
                yield f"data: {json.dumps({'type': 'chunk', 'content': char})}\n\n"
                await asyncio.sleep(0.02)
            if departments:
                yield f"data: {json.dumps({'type': 'departments', 'data': departments})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            session["messages"].append({"role": "assistant", "content": ai_response})

        return StreamingResponse(generate_sse(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"流式响应失败: {str(e)}")


def analyze_symptoms(message: str) -> list:
    """分析症状并推荐科室"""
    try:
        departments = load_departments()
        symptom_disease_map = load_symptom_disease()

        symptoms = [s for s in symptom_disease_map.keys() if s in message]
        if not symptoms:
            return []

        disease_count = {}
        for symptom in symptoms:
            for disease in symptom_disease_map.get(symptom, []):
                disease_count[disease] = disease_count.get(disease, 0) + 1

        dept_score = {}
        for disease, count in disease_count.items():
            for dept in departments:
                if disease in dept.get("common_diseases", []):
                    if dept["name"] not in dept_score:
                        dept_score[dept["name"]] = {"score": 0, "diseases": []}
                    dept_score[dept["name"]]["score"] += count
                    dept_score[dept["name"]]["diseases"].append(disease)

        results = []
        for dept_name, info in dept_score.items():
            confidence = min(0.95, 0.6 + info["score"] * 0.1)
            results.append({
                "name": dept_name,
                "confidence": round(confidence, 2),
                "reason": f"根据您描述的症状，可能患有{'、'.join(info['diseases'][:3])}等疾病"
            })

        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results[:3]

    except Exception as e:
        print(f"分析症状失败: {e}")
        return []


def generate_response(message: str, departments: list) -> str:
    """生成 AI 回复"""
    if not departments:
        return "您好！请详细描述您的症状，我会帮您推荐合适的科室和医生。"

    response = f"根据您描述的症状，我为您推荐以下科室：\n\n"
    for i, dept in enumerate(departments, 1):
        response += f"{i}. {dept['name']}（置信度：{dept['confidence']*100:.0f}%）\n"
        response += f"   {dept.get('reason', '')}\n"

    response += "\n您是否需要查询该科室的医生排班和费用估算？"
    return response
```

### 4.4 编写主入口 `main.py`

右键 `backend/app` → **`New → Python File`** → 输入 `main.py`：

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

# CORS 配置（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 前端静态文件服务（从 backend/static/ 目录）
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
static_path = os.path.abspath(static_path)

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

    @app.get("/")
    async def root():
        return FileResponse(os.path.join(static_path, "index.html"))
else:
    @app.get("/")
    async def root():
        return {
            "message": "医院智能导诊系统 API",
            "version": "1.0.0",
            "endpoints": {"docs": "/docs"}
        }

# 注册路由
from app.api import chat, department, doctor, cost
app.include_router(chat.router, prefix="/api/v1/chat", tags=["对话管理"])
app.include_router(department.router, prefix="/api/v1/department", tags=["科室推荐"])
app.include_router(doctor.router, prefix="/api/v1/doctors", tags=["医生查询"])
app.include_router(cost.router, prefix="/api/v1/cost", tags=["费用医保"])
```

### ✅ 本章验证

在 PyCharm 终端执行：

```bash
cd backend
python -c "from app.main import app; print('所有模块导入成功')"
```

如果输出"成功"，说明代码编写正确。

---

## 第 5 章：运行与调试后端

### 5.1 方式一：PyCharm 终端运行（最简单）

1. 点击底部 **Terminal** 标签
2. 确保在 `backend` 目录下（如果不在，执行 `cd backend`）
3. 运行命令：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. 看到以下输出表示启动成功：

```
INFO:     Will watch for changes in these directories: ['C:\...\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxx] using WatchFiles
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

5. **停止服务器**：在终端按 `Ctrl+C`

### 5.2 方式二：配置 PyCharm 运行配置（推荐）

这种方式可以利用 PyCharm 的调试功能（断点、变量查看等）。

#### 步骤 1：创建运行配置

1. 点击右上角运行按钮旁的下拉框 → **`Edit Configurations...`**

```
┌──────────────────────────────────────┐
│  Run/Debug Configurations            │
│                                      │
│  ┌─+─┐                              │
│  │   │ Python                        │
│  │   │                               │
│  └───┘                               │
│                                      │
│  Name:     [运行 uvicorn          ]  │
│  Script:   [uvicorn               ]  │
│  Parameters: [app.main:app --reload] │
│  Working dir: [C:\...\backend     ]  │
│  Python interpreter: [Python 3.10]  │
│                                      │
│  [OK] [Cancel] [Apply]              │
└──────────────────────────────────────┘
```

2. 点击左上角 **`+`** → 选择 **`Python`**
3. 填写配置信息：

| 字段 | 值 |
|------|-----|
| **Name** | `运行后端` |
| **Script path** | 点击文件夹图标，选择 `backend/venv/Scripts/uvicorn.exe`（Windows）或 `backend/venv/bin/uvicorn`（Mac） |
| **Parameters** | `app.main:app --reload --host 0.0.0.0 --port 8000` |
| **Working directory** | 选择 `backend` 目录 |
| **Python interpreter** | 选择项目的虚拟环境 |

4. 点击 **OK** 保存

#### 步骤 2：运行

点击右上角绿色三角形 **▶** 按钮，或按 `Shift+F10`

```
  [运行后端 ▼]  ▶  🐛  │  医院智能导诊系统
```

#### 步骤 3：调试（设置断点）

1. 在代码行号左侧点击，出现红点（断点）：

```
24│    departments = load_departments()           ← 普通行
25│    symptom_disease_map = load_symptom_disease()  ← 普通行
26│    🔴 symptoms = []                           ← 红点 = 断点
27│    for symptom in symptom_disease_map.keys():
```

2. 点击右上角 **🐛 调试按钮**，或按 `Shift+F9`
3. 程序运行到断点处暂停，你可以：
   - 查看变量值（底部 Variables 面板）
   - 单步执行（F8：Step Over，F7：Step Into）
   - 继续运行到下一个断点（F9：Resume）

### 5.3 方式三：在 main.py 中添加启动代码

在 `main.py` 末尾添加：

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

然后右键 `main.py` → **`Run 'main'`**，或直接在编辑区按 `Ctrl+Shift+F10`。

### 5.4 访问 API 文档

启动成功后，打开浏览器访问：

```
http://localhost:8000/docs
```

你会看到 FastAPI 自动生成的 **Swagger UI** 交互式文档：

```
┌──────────────────────────────────────────────────────┐
│  医院智能导诊系统 API                    v1.0.0      │
│  基于ReAct与RAG的医院智能导诊问答系统                │
│                                                       │
│  对话管理                                              │
│  ├── POST /api/v1/chat/session     创建新会话         │
│  ├── POST /api/v1/chat/send        发送消息（非流式）  │
│  └── GET  /api/v1/chat/stream      发送消息（SSE流式）│
│                                                       │
│  科室推荐                                              │
│  └── POST /api/v1/department/recommend               │
│                                                       │
│  医生查询                                              │
│  └── GET  /api/v1/doctors                            │
│                                                       │
│  费用医保                                              │
│  └── POST /api/v1/cost/estimate                     │
└──────────────────────────────────────────────────────┘
```

### ✅ 本章验证

- [ ] 后端能正常启动，终端显示 `Application startup complete`
- [ ] 浏览器访问 `http://localhost:8000/docs` 能看到 API 文档
- [ ] `--reload` 参数生效（修改代码后自动重启）

---

## 第 6 章：API 接口测试

### 6.1 使用 Swagger UI（推荐初学者）

在浏览器打开 `http://localhost:8000/docs`，可以直接在页面上测试每个 API。

#### 测试科室推荐

1. 找到 `POST /api/v1/department/recommend`，点击展开
2. 点击 **`Try it out`** 按钮
3. 在 Request body 中输入：

```json
{
  "symptoms": "头痛、头晕"
}
```

4. 点击 **`Execute`** 按钮
5. 查看 Response：

```json
{
  "departments": [
    {
      "name": "神经内科",
      "confidence": 0.7,
      "reason": "根据您描述的症状，可能患有偏头痛、紧张性头痛、脑梗死等疾病，建议就诊神经内科"
    }
  ],
  "reason": "根据您描述的症状（头痛,头晕），为您推荐以下科室"
}
```

#### 测试医生查询

1. 找到 `GET /api/v1/doctors`
2. 点击 `Try it out`
3. 在 `department` 参数中输入 `神经内科`
4. 点击 `Execute`

#### 测试费用估算

1. 找到 `POST /api/v1/cost/estimate`
2. 输入 `{"department": "呼吸内科"}`
3. 执行后查看总费用、医保支付、自费金额

### 6.2 使用 PyCharm 终端测试

在 PyCharm 底部 **Terminal** 中，使用 `curl` 命令测试：

**Windows (CMD)：**

```cmd
curl -X POST http://localhost:8000/api/v1/department/recommend -H "Content-Type: application/json" -d "{\"symptoms\": \"头痛、头晕\"}"
```

**Mac/Linux：**

```bash
curl -X POST http://localhost:8000/api/v1/department/recommend \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "头痛、头晕"}'
```

### 6.3 使用 PyCharm Python Console 测试

PyCharm 底部有 **Python Console** 标签，可以直接运行 Python 代码测试：

```python
import requests

# 测试科室推荐
resp = requests.post(
    "http://localhost:8000/api/v1/department/recommend",
    json={"symptoms": "发热、咳嗽"}
)
print(resp.json())

# 测试医生查询
resp = requests.get(
    "http://localhost:8000/api/v1/doctors",
    params={"department": "呼吸内科"}
)
print(resp.json())

# 测试费用估算
resp = requests.post(
    "http://localhost:8000/api/v1/cost/estimate",
    json={"department": "呼吸内科"}
)
print(resp.json())
```

### 6.4 使用 PyCharm 的 HTTP Client（Professional 版）

> PyCharm Professional 版内置了 HTTP Client，可以直接在 IDE 中发送 HTTP 请求。

1. 创建 `.http` 文件：右键项目 → **`New → HTTP Request`**
2. 输入请求内容：

```http
### 测试科室推荐
POST http://localhost:8000/api/v1/department/recommend
Content-Type: application/json

{
  "symptoms": "头痛、头晕"
}

### 测试医生查询
GET http://localhost:8000/api/v1/doctors?department=神经内科

### 测试费用估算
POST http://localhost:8000/api/v1/cost/estimate
Content-Type: application/json

{
  "department": "呼吸内科"
}
```

3. 点击每个请求旁边的绿色 ▶ 按钮执行
4. 响应结果会显示在右侧面板

```
┌──────────────────────┬─────────────────────────┐
│  test.http           │  Response               │
│                      │                         │
│  ### 测试科室推荐     │  HTTP/1.1 200 OK        │
│  POST http://...      │  Content-Type: app/json │
│  ...                  │                         │
│  ▶                   │  {                      │
│                      │    "departments": [...] │
│                      │  }                      │
└──────────────────────┴─────────────────────────┘
```

### ✅ 本章验证

- [ ] Swagger UI 能成功调用所有 4 个 API
- [ ] 输入"头痛"能返回"神经内科"推荐
- [ ] 输入"呼吸内科"能查到刘伟医生
- [ ] 费用估算能返回正确的总费用和医保金额

---

## 第 7 章：编写前端代码

> **为什么用纯 HTML 而不用 React/Vue？** 零构建配置、易学、够用。这个项目界面简单，纯 JS 完全能实现。

### 7.1 在 PyCharm 中创建前端文件

在左侧 Project 视图中，依次创建以下文件（右键目录 → `New → File`）：

```
frontend/
├── index.html       ← 右键 frontend → New → File
├── css/
│   └── style.css    ← 右键 css → New → File
└── js/
    ├── utils.js      ← 右键 js → New → File
    ├── api.js        ← 右键 js → New → File
    ├── components.js ← 右键 js → New → File
    └── chat.js       ← 右键 js → New → File
```

> **PyCharm 提示**：创建 `.html`、`.css`、`.js` 文件时，PyCharm 会自动识别文件类型并提供语法高亮和自动补全。

### 7.2 编写 `frontend/index.html`

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
        <header class="app-header">
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">🏥</span>
                    <h1>医院智能导诊系统</h1>
                </div>
                <div class="header-actions">
                    <button id="btn-clear" class="btn-secondary">清空</button>
                </div>
            </div>
        </header>

        <main class="main-content">
            <section class="chat-section">
                <div class="chat-container">
                    <div id="message-list" class="message-list">
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

                    <div class="input-section">
                        <div class="input-container">
                            <textarea id="user-input" class="user-input"
                                placeholder="请描述您的症状，例如：发热、咳嗽、头痛..." rows="2"></textarea>
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

            <aside class="result-section">
                <div class="result-card" id="department-result" style="display:none;">
                    <h3 class="result-title"><span class="result-icon">📍</span>推荐科室</h3>
                    <div class="result-content" id="department-list"></div>
                </div>
                <div class="result-card" id="doctor-result" style="display:none;">
                    <h3 class="result-title"><span class="result-icon">👨‍⚕️</span>推荐医生</h3>
                    <div class="result-content" id="doctor-list"></div>
                </div>
                <div class="result-card" id="cost-result" style="display:none;">
                    <h3 class="result-title"><span class="result-icon">💰</span>费用估算</h3>
                    <div class="result-content" id="cost-detail"></div>
                </div>
                <div class="help-card">
                    <h3 class="result-title"><span class="result-icon">💡</span>使用提示</h3>
                    <ul class="help-list">
                        <li>描述症状时，尽量详细具体</li>
                        <li>可以一次描述多个症状</li>
                        <li>系统会推荐科室、医生和预估费用</li>
                    </ul>
                </div>
            </aside>
        </main>
    </div>

    <script src="js/utils.js"></script>
    <script src="js/api.js"></script>
    <script src="js/components.js"></script>
    <script src="js/chat.js"></script>
</body>
</html>
```

> **注意脚本加载顺序！** `utils.js` → `api.js` → `components.js` → `chat.js`，因为后面的文件依赖前面的。

### 7.3 编写 `frontend/css/style.css`

```css
* { margin: 0; padding: 0; box-sizing: border-box; }

:root {
    --primary-color: #1890ff;
    --primary-hover: #40a9ff;
    --success-color: #52c41a;
    --warning-color: #faad14;
    --text-primary: #262626;
    --text-secondary: #8c8c8c;
    --bg-primary: #f0f2f5;
    --bg-white: #ffffff;
    --border-color: #d9d9d9;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 2px 8px rgba(0,0,0,0.1);
    --radius-md: 8px;
    --radius-lg: 12px;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
}

.app-container { max-width: 1400px; margin: 0 auto; min-height: 100vh; display: flex; flex-direction: column; }

.app-header { background: var(--bg-white); border-bottom: 1px solid var(--border-color); padding: 16px 24px; box-shadow: var(--shadow-sm); }
.header-content { display: flex; justify-content: space-between; align-items: center; }
.logo { display: flex; align-items: center; gap: 12px; }
.logo-icon { font-size: 32px; }
.logo h1 { font-size: 24px; font-weight: 600; }

.main-content { display: flex; gap: 24px; padding: 24px; flex: 1; }
.chat-section { flex: 1; min-width: 0; }
.chat-container { background: var(--bg-white); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); height: calc(100vh - 140px); display: flex; flex-direction: column; }

.message-list { flex: 1; overflow-y: auto; padding: 24px; }
.message { display: flex; gap: 12px; margin-bottom: 20px; animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.message-avatar { width: 40px; height: 40px; border-radius: 50%; background: var(--bg-primary); display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
.message-content { flex: 1; min-width: 0; }
.message-text { background: var(--bg-primary); padding: 12px 16px; border-radius: var(--radius-md); line-height: 1.6; word-wrap: break-word; }
.message.assistant .message-text { background: #e6f7ff; }
.message.user { flex-direction: row-reverse; }
.message.user .message-text { background: var(--primary-color); color: white; }

.input-section { padding: 16px 24px; border-top: 1px solid var(--border-color); }
.input-container { display: flex; gap: 12px; margin-bottom: 12px; }
.user-input { flex: 1; padding: 12px 16px; border: 1px solid var(--border-color); border-radius: var(--radius-md); font-size: 14px; resize: none; font-family: inherit; }
.user-input:focus { outline: none; border-color: var(--primary-color); }

.btn-primary { padding: 12px 24px; background: var(--primary-color); color: white; border: none; border-radius: var(--radius-md); font-size: 14px; cursor: pointer; white-space: nowrap; }
.btn-primary:hover { background: var(--primary-hover); }
.btn-primary:disabled { background: var(--border-color); cursor: not-allowed; }
.btn-secondary { padding: 8px 16px; background: var(--bg-white); border: 1px solid var(--border-color); border-radius: 4px; font-size: 14px; cursor: pointer; }
.btn-secondary:hover { color: var(--primary-color); border-color: var(--primary-color); }

.input-hints { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.hint-label { font-size: 12px; color: var(--text-secondary); }
.hint-btn { padding: 4px 12px; background: var(--bg-primary); border: none; border-radius: 20px; font-size: 12px; color: var(--text-secondary); cursor: pointer; }
.hint-btn:hover { background: var(--primary-color); color: white; }

.result-section { width: 360px; flex-shrink: 0; display: flex; flex-direction: column; gap: 16px; }
.result-card { background: var(--bg-white); border-radius: var(--radius-lg); padding: 20px; box-shadow: var(--shadow-md); animation: slideIn 0.3s ease; }
@keyframes slideIn { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
.result-title { font-size: 16px; font-weight: 600; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.result-icon { font-size: 20px; }

.department-card { padding: 16px; border: 1px solid var(--border-color); border-radius: var(--radius-md); margin-bottom: 12px; cursor: pointer; }
.department-card:hover { border-color: var(--primary-color); }
.department-name { font-size: 16px; font-weight: 600; margin-bottom: 8px; display: flex; justify-content: space-between; }
.confidence-bar { height: 6px; background: var(--bg-primary); border-radius: 3px; margin: 8px 0; overflow: hidden; }
.confidence-fill { height: 100%; background: var(--primary-color); border-radius: 3px; transition: width 0.5s ease; }
.department-reason { font-size: 13px; color: var(--text-secondary); }

.doctor-card { padding: 16px; border: 1px solid var(--border-color); border-radius: var(--radius-md); margin-bottom: 12px; }
.doctor-header { display: flex; justify-content: space-between; margin-bottom: 8px; }
.doctor-name { font-size: 16px; font-weight: 600; }
.doctor-title { font-size: 12px; color: var(--primary-color); background: #e6f7ff; padding: 2px 8px; border-radius: 10px; }
.doctor-info { font-size: 13px; color: var(--text-secondary); margin-bottom: 4px; }
.doctor-schedule { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
.schedule-tag { padding: 2px 8px; background: var(--bg-primary); border-radius: 10px; font-size: 12px; color: var(--text-secondary); }
.schedule-tag.available { background: #f6ffed; color: var(--success-color); }

.cost-summary { display: flex; justify-content: space-between; margin-bottom: 16px; padding: 16px; background: var(--bg-primary); border-radius: var(--radius-md); }
.cost-item { text-align: center; }
.cost-label { font-size: 12px; color: var(--text-secondary); margin-bottom: 4px; }
.cost-value { font-size: 20px; font-weight: 600; }
.cost-value.total { color: var(--primary-color); }
.cost-value.insurance { color: var(--success-color); }
.cost-value.self-pay { color: var(--warning-color); }
.breakdown-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--bg-primary); font-size: 14px; }
.insurance-policy { margin-top: 16px; padding: 12px; background: #fff7e6; border-radius: 4px; font-size: 13px; color: #d48806; }

.help-card { background: var(--bg-white); border-radius: var(--radius-lg); padding: 20px; box-shadow: var(--shadow-md); }
.help-list { list-style: none; }
.help-list li { padding: 8px 0; font-size: 14px; color: var(--text-secondary); }
.help-list li:before { content: "•"; color: var(--primary-color); font-weight: bold; margin-right: 8px; }

.loading-dots { display: inline-flex; gap: 4px; }
.loading-dots span { width: 8px; height: 8px; background: var(--text-secondary); border-radius: 50%; animation: loading 1.4s ease-in-out infinite; }
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes loading { 0%,80%,100% { transform: scale(0.6); opacity: 0.4; } 40% { transform: scale(1); opacity: 1; } }

@media (max-width: 1024px) { .main-content { flex-direction: column; } .result-section { width: 100%; } .chat-container { height: 60vh; } }
```

### 7.4 编写 `frontend/js/utils.js`

```javascript
function formatTime(date = new Date()) {
    return `${date.getHours().toString().padStart(2,'0')}:${date.getMinutes().toString().padStart(2,'0')}`;
}

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

function scrollToBottom(element) { element.scrollTop = element.scrollHeight; }

function createElement(tag, attributes = {}, children = []) {
    const element = document.createElement(tag);
    for (const [key, value] of Object.entries(attributes)) {
        if (key === 'className') element.className = value;
        else if (key === 'textContent') element.textContent = value;
        else if (key === 'innerHTML') element.innerHTML = value;
        else if (key.startsWith('on')) element.addEventListener(key.toLowerCase().slice(2), value);
        else element.setAttribute(key, value);
    }
    if (Array.isArray(children)) {
        children.forEach(child => {
            if (typeof child === 'string') element.appendChild(document.createTextNode(child));
            else if (child instanceof HTMLElement) element.appendChild(child);
        });
    }
    return element;
}

window.utils = { formatTime, setLoading, scrollToBottom, createElement };
```

### 7.5 编写 `frontend/js/api.js`

```javascript
// 如果前端由后端静态服务托管（同源），用空字符串
// 如果前端单独运行（不同端口），改为 'http://localhost:8000'
const API_BASE_URL = '';

async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const finalOptions = { headers: { 'Content-Type': 'application/json' }, ...options };
    try {
        const response = await fetch(url, finalOptions);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

async function recommendDepartment(symptoms) {
    return await apiRequest('/api/v1/department/recommend', { method: 'POST', body: JSON.stringify({ symptoms }) });
}

async function searchDoctors(department, scheduleDay = null) {
    const params = new URLSearchParams({ department });
    if (scheduleDay) params.append('schedule_day', scheduleDay);
    return await apiRequest(`/api/v1/doctors?${params.toString()}`);
}

async function estimateCost(department) {
    return await apiRequest('/api/v1/cost/estimate', { method: 'POST', body: JSON.stringify({ department }) });
}

window.api = { recommendDepartment, searchDoctors, estimateCost };
```

### 7.6 编写 `frontend/js/components.js`

```javascript
function renderDepartmentCards(departments) {
    const container = document.getElementById('department-list');
    container.innerHTML = '';
    departments.forEach(dept => {
        container.appendChild(utils.createElement('div', { className: 'department-card' }, [
            utils.createElement('div', { className: 'department-name' }, [
                utils.createElement('span', { textContent: dept.name }),
                utils.createElement('span', { textContent: `${(dept.confidence*100).toFixed(0)}%`, style: 'color:#1890ff;' }),
            ]),
            utils.createElement('div', { className: 'confidence-bar' }, [
                utils.createElement('div', { className: 'confidence-fill', style: `width:${dept.confidence*100}%` })
            ]),
            utils.createElement('div', { className: 'department-reason', textContent: dept.reason }),
        ]));
    });
}

function renderDoctorCards(doctors) {
    const container = document.getElementById('doctor-list');
    container.innerHTML = '';
    doctors.forEach(doctor => {
        const card = utils.createElement('div', { className: 'doctor-card' }, [
            utils.createElement('div', { className: 'doctor-header' }, [
                utils.createElement('div', { className: 'doctor-name', textContent: doctor.name }),
                utils.createElement('span', { className: 'doctor-title', textContent: doctor.title }),
            ]),
            utils.createElement('div', { className: 'doctor-info', textContent: `科室：${doctor.department}` }),
            utils.createElement('div', { className: 'doctor-info', textContent: `专长：${doctor.specialty}` }),
            utils.createElement('div', { className: 'doctor-info', textContent: `评分：${'⭐'.repeat(Math.floor(doctor.rating))} (${doctor.rating})` }),
            utils.createElement('div', { className: 'doctor-info', textContent: `从业：${doctor.experience_years}年` }),
        ]);
        if (doctor.schedule) {
            const schedDiv = utils.createElement('div', { className: 'doctor-schedule' });
            for (const [day, time] of Object.entries(doctor.schedule)) {
                schedDiv.appendChild(utils.createElement('span', { className: `schedule-tag ${time!=='休息'?'available':''}`, textContent: `${day}: ${time}` }));
            }
            card.appendChild(schedDiv);
        }
        container.appendChild(card);
    });
}

function renderCostDetail(costData) {
    const container = document.getElementById('cost-detail');
    container.innerHTML = '';
    container.appendChild(utils.createElement('div', { className: 'cost-summary' }, [
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
    ]));
    if (costData.breakdown) {
        const list = utils.createElement('div', { className: 'cost-breakdown' });
        costData.breakdown.forEach(item => {
            list.appendChild(utils.createElement('div', { className: 'breakdown-item' }, [
                utils.createElement('span', { textContent: item.name }),
                utils.createElement('span', { textContent: `¥${item.price} (医保${item.insurance_rate*100}%)` }),
            ]));
        });
        container.appendChild(list);
    }
    if (costData.insurance_policy) {
        container.appendChild(utils.createElement('div', { className: 'insurance-policy', textContent: costData.insurance_policy }));
    }
}

function showResultCard(id) { document.getElementById(id).style.display = 'block'; }
function hideResultCard(id) { document.getElementById(id).style.display = 'none'; }

window.components = { renderDepartmentCards, renderDoctorCards, renderCostDetail, showResultCard, hideResultCard };
```

### 7.7 编写 `frontend/js/chat.js`

```javascript
let sessionId = null;
let isProcessing = false;

function initChat() {
    sessionId = `session_${Date.now()}`;
    bindEvents();
}

function bindEvents() {
    const input = document.getElementById('user-input');
    document.getElementById('btn-send').addEventListener('click', sendMessage);
    input.addEventListener('keypress', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } });
    document.getElementById('btn-clear').addEventListener('click', clearChat);
    document.querySelectorAll('.hint-btn').forEach(btn => {
        btn.addEventListener('click', () => { input.value = btn.dataset.text; input.focus(); });
    });
}

async function sendMessage() {
    if (isProcessing) return;
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    appendMessage('user', message);
    input.value = '';
    isProcessing = true;
    utils.setLoading(document.getElementById('btn-send'), true);
    appendLoadingMessage();

    try {
        // 1. 调用科室推荐
        const deptResult = await api.recommendDepartment(message);
        components.renderDepartmentCards(deptResult.departments);
        components.showResultCard('department-result');

        // 2. 并行查询医生和费用
        if (deptResult.departments?.length > 0) {
            const topDept = deptResult.departments[0].name;
            const [doctorResult, costResult] = await Promise.all([
                api.searchDoctors(topDept),
                api.estimateCost(topDept),
            ]);
            if (doctorResult.doctors?.length > 0) {
                components.renderDoctorCards(doctorResult.doctors);
                components.showResultCard('doctor-result');
            }
            components.renderCostDetail(costResult);
            components.showResultCard('cost-result');
        }

        // 3. 显示 AI 回复
        removeLoadingMessage();
        appendMessage('assistant', generateReplyText(deptResult));
    } catch (error) {
        removeLoadingMessage();
        appendMessage('assistant', `抱歉，处理出错：${error.message}`);
    } finally {
        isProcessing = false;
        utils.setLoading(document.getElementById('btn-send'), false);
    }
}

function generateReplyText(deptResult) {
    let text = (deptResult.reason || '') + '\n\n推荐科室：\n';
    deptResult.departments?.forEach((dept, i) => {
        text += `${i+1}. ${dept.name} (置信度 ${(dept.confidence*100).toFixed(0)}%)\n   ${dept.reason}\n`;
    });
    text += '\n已为您查询医生和费用，请查看右侧详情。';
    return text;
}

function appendMessage(role, text) {
    const list = document.getElementById('message-list');
    list.appendChild(utils.createElement('div', { className: `message ${role}` }, [
        utils.createElement('div', { className: 'message-avatar' }, [role === 'user' ? '👤' : '🤖']),
        utils.createElement('div', { className: 'message-content' }, [
            utils.createElement('div', { className: 'message-text', textContent: text }),
        ]),
    ]));
    utils.scrollToBottom(list);
}

function appendLoadingMessage() {
    const list = document.getElementById('message-list');
    list.appendChild(utils.createElement('div', { className: 'message assistant', id: 'loading-message' }, [
        utils.createElement('div', { className: 'message-avatar' }, ['🤖']),
        utils.createElement('div', { className: 'message-content' }, [
            utils.createElement('div', { className: 'loading-dots' }, [
                utils.createElement('span'), utils.createElement('span'), utils.createElement('span'),
            ]),
        ]),
    ]));
    utils.scrollToBottom(list);
}

function removeLoadingMessage() { document.getElementById('loading-message')?.remove(); }

function clearChat() {
    const list = document.getElementById('message-list');
    const first = list.querySelector('.message');
    list.innerHTML = '';
    if (first) list.appendChild(first);
    ['department-result', 'doctor-result', 'cost-result'].forEach(hideResultCard);
    sessionId = `session_${Date.now()}`;
}

document.addEventListener('DOMContentLoaded', initChat);
```

> **对话流程图**：
> ```
> 用户输入"头痛" → appendMessage('user') → 显示加载动画
>   → api.recommendDepartment("头痛") → 渲染科室卡片
>   → Promise.all([查医生, 查费用]) → 渲染医生卡 + 费用卡
>   → 移除加载动画 → appendMessage('assistant', 回复)
> ```

### ✅ 本章验证

- [ ] 6 个前端文件都已创建
- [ ] PyCharm 中各文件无红色波浪线（语法正确）

---

## 第 8 章：前后端联调

### 8.1 将前端复制到后端静态目录

> **为什么要复制？** FastAPI 配置了从 `backend/static/` 目录提供前端文件。这样只需启动后端，浏览器访问 `http://localhost:8000/` 就能直接看到前端页面，且不存在跨域问题。

在 PyCharm 终端执行：

```bash
# Windows:
xcopy /E /I /Y frontend\* backend\static\

# Mac/Linux:
cp -r frontend/* backend/static/
```

或者在 PyCharm 中手动操作：
1. 选中 `frontend` 下的所有文件和文件夹
2. `Ctrl+C` 复制
3. 进入 `backend/static/` 目录
4. `Ctrl+V` 粘贴

### 8.2 修改 `api.js` 的 API 地址

> 如果前端由后端托管（同源），`API_BASE_URL` 应设为空字符串（用相对路径）。

打开 `backend/static/js/api.js`，确认第 3 行：

```javascript
const API_BASE_URL = '';  // 空字符串 = 同源访问
```

> 如果你单独用浏览器打开 `frontend/index.html`（非后端托管），则需要改为：
> ```javascript
> const API_BASE_URL = 'http://localhost:8000';
> ```

### 8.3 启动后端

确保后端正在运行（第 5 章）。如果没运行，在 PyCharm 终端：

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 8.4 浏览器访问

打开浏览器，访问：

```
http://localhost:8000
```

### 8.5 完整测试

1. **输入症状**：在输入框输入"头痛、头晕"
2. **发送**：点击发送按钮或按回车
3. **查看结果**：
   - 左侧：你的消息 + AI 回复
   - 右侧：科室卡片 → 医生卡片 → 费用卡片
4. **快速输入**：点击"发热咳嗽"等按钮快速填入
5. **清空**：点击右上角"清空"重置

### 8.6 PyCharm 中实时修改代码

`--reload` 参数让后端在代码修改后自动重启。你可以：

1. 修改 `api/department.py` 中的推荐逻辑
2. 保存（`Ctrl+S`）
3. 终端会显示 `WatchFiles detected changes... Reloading...`
4. 刷新浏览器查看效果

修改前端文件后，直接刷新浏览器即可（`F5`）。

### 8.7 使用 PyCharm 调试前后端

1. 在 `department.py` 的 `recommend_department` 函数中设置断点（行号旁点击）
2. 用调试模式运行后端（`Shift+F9`）
3. 在浏览器输入症状发送
4. 程序会在断点处暂停
5. 在底部 **Variables** 面板查看 `request.symptoms`、`symptoms`、`dept_score` 等变量值
6. 按 `F8` 单步执行，`F9` 继续运行

```
┌─ Debug ──────────────────────────────────────────────┐
│  Frames    Variables          Console                │
│                                                      │
│  recommend_department                                 │
│    request = DepartmentRecommendRequest(symptoms=..) │
│    symptoms = ['头痛', '头晕']                       │
│    disease_count = {'偏头痛':1, '高血压':2, ...}      │
│    dept_score = {'神经内科':{...}, '心血管内科':{..}} │
│                                                      │
│  [▶ Resume] [⬇ Step Over] [⬇ Step Into] [⬹ Stop]   │
└──────────────────────────────────────────────────────┘
```

### ✅ 本章验证

- [ ] 浏览器 `http://localhost:8000` 能看到系统界面
- [ ] 输入症状后右侧能显示推荐卡片
- [ ] 修改代码保存后，刷新浏览器能看到变化
- [ ] PyCharm 断点调试能正常工作

---

## 第 9 章：Docker 部署（可选）

> 如果只想本地运行，可以跳过这章。Docker 部署适合上线或给他人使用。

### 9.1 创建 Docker 配置文件

在 PyCharm 中创建以下文件（右键目录 → New → File）：

#### `backend/Dockerfile`

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装 gcc（部分 Python 包编译需要）
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制代码
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

#### `frontend/Dockerfile`

```dockerfile
FROM nginx:alpine

COPY . /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### `frontend/nginx.conf`

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # 取消注释以启用 API 反向代理
    # location /api/ {
    #     proxy_pass http://backend:8000;
    #     proxy_set_header Host $host;
    #     proxy_set_header X-Real-IP $remote_addr;
    # }
}
```

#### 项目根目录 `docker-compose.yml`

右键项目根目录 → New → File → `docker-compose.yml`：

```yaml
version: '3.8'

services:
  backend:
    container_name: guide-backend
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - USE_MOCK=true
    volumes:
      - ./backend:/app
    restart: unless-stopped

  frontend:
    container_name: guide-frontend
    build: ./frontend
    ports:
      - "8080:80"
    depends_on:
      - backend
    restart: unless-stopped
```

> **简化说明**：这里只启动后端和前端两个服务。如果需要 Milvus 向量数据库（进阶 RAG 功能），请参考 TUTORIAL.md 的完整版本。

#### `.env.example`

```env
# OpenAI API Key（可选）
# OPENAI_API_KEY=sk-your-api-key

# 是否使用 Mock 模式（true = 规则引擎，不调 LLM）
USE_MOCK=true
```

### 9.2 在 PyCharm 终端启动 Docker

```bash
# 复制环境变量模板
cp .env.example .env

# 构建并启动
docker-compose up -d --build

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f backend

# 停止
docker-compose down
```

### 9.3 访问

- 前端：`http://localhost:8080`
- 后端 API：`http://localhost:8000/docs`

### ✅ 本章验证

- [ ] `docker-compose ps` 显示两个服务都是 running
- [ ] `http://localhost:8080` 能看到前端页面
- [ ] `http://localhost:8000/docs` 能看到 API 文档

---

## 附录 A：PyCharm 常用快捷键

### Windows/Linux

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+N` | 查找类/文件 |
| `Ctrl+Shift+N` | 按文件名搜索 |
| `Ctrl+B` | 跳转到定义（光标放在函数/变量上） |
| `Alt+F7` | 查找用法 |
| `Ctrl+/` | 注释/取消注释当前行 |
| `Ctrl+D` | 复制当前行 |
| `Ctrl+Y` | 删除当前行 |
| `Ctrl+Alt+L` | 格式化代码 |
| `Shift+F10` | 运行 |
| `Shift+F9` | 调试 |
| `F8` | 单步执行（Step Over） |
| `F7` | 进入函数（Step Into） |
| `F9` | 继续运行到下一个断点 |
| `Alt+1` | 显示/隐藏 Project 视图 |
| `Ctrl+F` | 当前文件搜索 |
| `Ctrl+R` | 当前文件替换 |
| `Ctrl+Shift+F` | 全局搜索 |

### Mac

| 快捷键 | 功能 |
|--------|------|
| `Cmd+N` | 查找类/文件 |
| `Cmd+Shift+O` | 按文件名搜索 |
| `Cmd+B` | 跳转到定义 |
| `Cmd+/` | 注释/取消注释 |
| `Cmd+D` | 复制当前行 |
| `Cmd+Alt+L` | 格式化代码 |
| `Ctrl+R` | 运行 |
| `Ctrl+D` | 调试 |
| `F8` | Step Over |
| `F7` | Step Into |
| `F9` | Resume |
| `Cmd+1` | 显示/隐藏 Project 视图 |

---

## 附录 B：常见问题排查

### B.1 `ModuleNotFoundError: No module named 'fastapi'`

**原因**：虚拟环境未激活，或依赖未安装。

**解决**：
1. PyCharm 底部打开 Terminal，确认命令行前有 `(venv)` 前缀
2. 如果没有，执行：
   - Windows: `venv\Scripts\activate`
   - Mac: `source venv/bin/activate`
3. 安装依赖：`pip install fastapi uvicorn[standard] pydantic`

### B.2 `Address already in use: port 8000`

**原因**：8000 端口被其他程序占用。

**解决**：
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /F /PID <进程ID>

# Mac/Linux:
lsof -i :8000
kill -9 <进程ID>

# 或者换端口：
uvicorn app.main:app --reload --port 8001
```

### B.3 `CORS error`（跨域错误）

**原因**：前端和后端不在同一个域名/端口。

**解决**：
1. 确认 `main.py` 中已配置 CORS 中间件
2. 或者将前端放在 `backend/static/` 目录，用后端托管（推荐）

### B.4 JSON 文件中文乱码

**原因**：文件编码不是 UTF-8。

**解决**：
1. 在 PyCharm 中打开 JSON 文件
2. 右下角点击编码（如 GBK）
3. 选择 `UTF-8` → `Convert`（转换为 UTF-8）

### B.5 PyCharm 代码补全不工作

**原因**：Python 解释器未正确配置。

**解决**：
1. `File → Settings → Project → Python Interpreter`
2. 确认选择了项目的虚拟环境
3. 等待 PyCharm 重新建立索引（右下角进度条）

### B.6 断点不生效

**原因**：使用了 `--reload` 模式，有时断点不工作。

**解决**：
1. 去掉 `--reload` 参数
2. 或者用 `if __name__ == "__main__"` 方式启动
3. 确认断点是红色实心圆（不是灰色空心圆）

### B.7 `--reload` 不自动重载

**原因**：文件可能在 PyCharm 之外被修改。

**解决**：
1. 确认在 PyCharm 中编辑文件
2. 保存后查看终端是否有 `WatchFiles detected changes` 输出
3. 如果没有，手动重启后端

---

## 附录 C：完整项目结构

```
hospital-guide/
├── .idea/                        ← PyCharm 配置
├── venv/                         ← Python 虚拟环境
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               ← FastAPI 主入口
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py           ← 对话管理
│   │   │   ├── cost.py           ← 费用估算
│   │   │   ├── department.py     ← 科室推荐
│   │   │   └── doctor.py         ← 医生查询
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py           ← 聊天模型
│   │   │   └── response.py       ← 响应模型
│   │   └── data/
│   │       ├── departments.json  ← 科室数据
│   │       ├── doctors.json      ← 医生数据
│   │       ├── symptom_disease.json ← 症状映射
│   │       └── cost_insurance.json  ← 费用数据
│   ├── static/                   ← 前端文件副本
│   │   ├── index.html
│   │   ├── css/style.css
│   │   └── js/
│   │       ├── api.js
│   │       ├── chat.js
│   │       ├── components.js
│   │       └── utils.js
│   ├── Dockerfile
│   └── requirements.txt
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
└── .env.example
```

---

> 🎉 **恭喜完成！** 你已经用 PyCharm 从零搭建了一个完整的医院智能导诊系统。
>
> **回顾你学到的**：
> - PyCharm 项目创建与虚拟环境配置
> - FastAPI 后端开发（路由、模型、中间件）
> - Pydantic 数据验证
> - JSON 数据处理
> - 纯 HTML/CSS/JS 前端开发
> - 前后端 fetch 通信
> - PyCharm 运行配置与断点调试
> - Swagger API 文档使用
> - Docker 容器化部署
>
> **下一步可以探索**：
> - 接入 OpenAI API 让推荐更智能
> - 添加用户登录和历史记录
> - 用数据库替换 JSON 文件
> - 部署到云服务器
